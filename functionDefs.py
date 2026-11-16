## Function definitions for the physics RSS feed reader.
from keywords import titlelist, wordlist, authors
import os
import re
import feedparser
import smtplib  # Import smtplib for the actual sending function
import socket
import time
import datetime as dt
from email.mime.text import MIMEText  # Import the email modules we'll need
from unicodedata import normalize

# feedparser has no timeout of its own; without this one unresponsive journal server can hang the whole run.
# A feed that times out shows up in the dead-feed warning instead.
socket.setdefaulttimeout(30)

cleanr = re.compile('<.*?>')

_nonDecomposing = str.maketrans({'ø': 'o', 'Ø': 'O', 'ł': 'l', 'Ł': 'L', 'đ': 'd', 'ß': 'ss', 'æ': 'ae', 'Æ': 'AE'})


def foldAccents(text):
    return normalize('NFKD', text.translate(_nonDecomposing)).encode('ascii', 'ignore').decode('ascii')


def myFormat(text):
    # Lowercase, fold accents, and turn hyphens/punctuation into single spaces for keyword matching,
    # so "Fault-Tolerant" -> "fault tolerant".
    return re.sub(r'[\W_]+', ' ', foldAccents(text).lower()).strip()


def keywordPattern(words):
    # Whole-word match with optional plural ("transmon" -> "transmons"); a trailing * makes it a prefix
    # ("error correct*" -> "error correction"). Either way "ion" won't match inside "dimension".
    alternatives = []
    for w in words:
        if w.endswith('*'):
            alternatives.append(re.escape(myFormat(w[:-1])))
        else:
            alternatives.append(re.escape(myFormat(w)) + r'(?:s|es)?\b')
    return re.compile(r'\b(?:' + '|'.join(alternatives) + ')')


titlePattern = keywordPattern(titlelist)
abstractPattern = keywordPattern(wordlist)


def myAuthorFormat(text):
    if text.strip() == '':
        return ''
    # Fold accents so "Müller", "M\"uller" (arXiv LaTeX) and "Muller" all compare equal.
    text = foldAccents(text)
    # Remove punctuation, capitalization for checking for matches to keywords.
    text = text.replace('.', ' ')  # sometimes initials aren't separated by spaces in listings
    text = text.replace('  ', ' ')  # remove any double spaces created by previous line
    formatted = re.sub(r'[^\w\s]', '', text.lower())
    formatted = formatted.strip()
    nameList = formatted.split(' ')
    firstInitLastNameOnly = ''
    try:
        firstInitLastNameOnly = nameList[0][0] + ' ' + nameList[-1]
    except IndexError:
        pass
    return firstInitLastNameOnly


def passes_filter(entry, latestExecutionDate, getVeryInterestingEntries):

    # Get author names from RSS entry, if possible... turns out the general case is not well defined and thus hard to handle!
    try:
        entryAuthors = entry.authors  # this line may throw an attribute error
        if {} in entryAuthors:
            raise AttributeError('')  # or the attribute in the RSS entry just may not contain the right info
    except AttributeError:
        try:
            entryAuthors = entry.author
        except AttributeError:
            entryAuthors = [""]
    if isinstance(entryAuthors, str):
        entryAuthors = [entryAuthors]
    entryAuthors2 = []
    for entryAuthor in entryAuthors:
        try:
            entryAuthor = entryAuthor['name']
        except (KeyError, TypeError):
            pass
        entryAuthor = re.sub(cleanr, '', entryAuthor)  # strips html tags
        entryAuthors2.extend(entryAuthor.split(','))  # break author lists apart by commas as needed, hopefully
    entryAuthors2 = [myAuthorFormat(entryAuthor) for entryAuthor in entryAuthors2]

    isVeryInteresting = any(myAuthorFormat(author) in entryAuthors2 for author in authors)
    if isVeryInteresting:
        isInteresting = False  # helps avoid duplicates listings in the summary produced.
    else:
        summary = entry.get('summary', '')
        title = entry.get('title', '')
        isInteresting = bool(abstractPattern.search(myFormat(strip_html(summary)))
                             or titlePattern.search(myFormat(strip_html(title))))

    # Get date of RSS entry, if possible
    # (dict.get bypasses feedparser's deprecated updated->published remapping)
    dateTuple = dict.get(entry, 'updated_parsed') or dict.get(entry, 'published_parsed')
    pubDate = int('%04d%02d%02d' % tuple(dateTuple[0:3])) if dateTuple else None

    announceType = entry.get('arxiv_announce_type')
    if announceType is not None:
        # arXiv feed (format since Jan 2024). Each entry is dated with the day of the announcement.
        # Keep new submissions and cross-lists; skip revised versions ('replace', 'replace-cross').
        # Strict '>' because the feed keeps Friday's listing over the weekend (skipDays).
        isNew = announceType in ('new', 'cross') and pubDate is not None and pubDate > latestExecutionDate
    elif pubDate is None:
        # Feed gives no dates; assume new on weekdays.
        isNew = dt.datetime.today().weekday() < 5
    else:
        isNew = pubDate >= latestExecutionDate

    if getVeryInterestingEntries:
        return isVeryInteresting and isNew
    else:
        return isInteresting and isNew


def strip_html(text):
    return re.sub('<[^<]+?>', '', text)


def arxivID(entry):
    # e.g. link 'https://arxiv.org/abs/2611.17417' -> '2611.17417' (version suffix dropped if present)
    return re.sub(r'v\d+$', '', entry.link.rstrip('/').split('/abs/')[-1])


def paperID(entry):
    # Key used to drop the same paper showing up in several feeds (arXiv quant-ph + cond-mat,
    # Nature main feed + Nature subject feed, ...).
    link = entry.get('link', '')
    if 'arxiv.org/abs/' in link:
        return 'arxiv:' + arxivID(entry)
    link = link.split('?')[0].split('#')[0].rstrip('/')
    return re.sub(r'^http://', 'https://', link)


_feedCache = {}


def fetchFeed(feedURL):
    # Each feed is downloaded once per run (it is used by both the author pass and the keyword pass).
    if feedURL not in _feedCache:
        try:
            _feedCache[feedURL] = feedparser.parse(feedURL)
        except Exception as e:
            _feedCache[feedURL] = feedparser.FeedParserDict(entries=[], bozo=1, bozo_exception=e)
    return _feedCache[feedURL]


def feedProblem(feedURL):
    # Returns a short description of what went wrong if a feed gave us nothing usable, else None.
    feed = fetchFeed(feedURL)
    status = feed.get('status')
    if status is not None and status >= 400:
        return 'HTTP error %d' % status
    if len(feed.entries) == 0:
        if feed.get('bozo'):
            return 'not a valid feed (%s)' % type(feed.get('bozo_exception')).__name__
        return 'feed is empty'
    return None


def cleanDescription(text):
    # arXiv abstracts start with "arXiv:2611.17417v1 Announce Type: new \nAbstract: "; drop that prefix.
    text = re.sub(r'^\s*arXiv:\S+\s+Announce Type:\s*\S+\s*Abstract:\s*', '', text)
    return strip_html(text)


def unicodeToAscii(uStr):
    # Strip accents etc. so the email body is plain ASCII (e.g. "Schrödinger" -> "Schrodinger").
    return foldAccents(uStr)


def executiveSummary(feedURL, feedNameString, latestExecutionDate, seenPaperIDs, getVeryInterestingEntries):
    # seenPaperIDs is shared across all feeds and both passes; papers already listed are skipped.
    print("Now checking: " + feedNameString)
    feed = fetchFeed(feedURL)

    filtered_entries = []
    for entry in feed.entries:
        if not passes_filter(entry, latestExecutionDate, getVeryInterestingEntries):
            continue
        thisID = paperID(entry)
        if thisID:
            if thisID in seenPaperIDs:
                continue
            seenPaperIDs.add(thisID)
        filtered_entries.append(entry)

    numFilteredEntries = len(filtered_entries)
    if numFilteredEntries == 0:
        return ('', 0)

    ## Assemble the large summary string:
    largestring = "--------------- " + feedNameString + " ---------------"
    largestring = largestring + "\n"

    for entry in filtered_entries:
        largestring += "\n" + strip_html(entry.get('title', '(no title)')) + "\n \n"
        if entry.get('author'):
            largestring += " \t" + strip_html(entry.author) + "\n"
        largestring += " \t" + entry.get('link', '') + "\n \n"
        description = cleanDescription(entry.get('description', '')).strip()
        if description:
            largestring += description + "\n"

    return (unicodeToAscii(largestring), numFilteredEntries)


def buildEmail(message, numVIentries, numOtherEntries, sender, recipient):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = "cQED Digest " + time.strftime("%m/%d/%Y") + " [" + str(numVIentries) + "," + str(numOtherEntries) + "]"
    msg['From'] = sender
    msg['To'] = recipient
    return msg


def sendSummaryEmails(recipientList, message, numVIentries, numOtherEntries):
    # SMTP settings come from environment variables so no password lives in the repo:
    #   SMTP_USER, SMTP_PASSWORD (required; for Gmail use an app password),
    #   SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 587), SMTP_SENDER (default SMTP_USER)
    username = os.environ.get('SMTP_USER')
    password = os.environ.get('SMTP_PASSWORD')
    if not username or not password:
        raise RuntimeError('Set the SMTP_USER and SMTP_PASSWORD environment variables to send email.')
    host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('SMTP_PORT', '587'))
    sender = os.environ.get('SMTP_SENDER', username)

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.login(username, password)

    for recipient in recipientList:
        msg = buildEmail(message, numVIentries, numOtherEntries, sender, recipient)
        s.sendmail(sender, [recipient], msg.as_string())

    s.quit()
