## Function definitions for the physics RSS feed reader.
from keywords import titlelist, wordlist, authors
import re
import feedparser
import smtplib  # Import smtplib for the actual sending function
import time
import datetime as dt
from email.mime.text import MIMEText  # Import the email modules we'll need
from unicodedata import normalize


def myFormat(text):
    # Remove punctuation, capitalization for checking for matches to keywords.
    return re.sub(r'[^\w\s]', '', text.lower())


cleanr = re.compile('<.*?>')


def myAuthorFormat(text):
    if text.strip() == '':
        return ''
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
        isInteresting = (any(myFormat(word) in myFormat(summary) for word in wordlist)
                         or any(myFormat(titleword) in myFormat(title) for titleword in titlelist))

    isArxiv = False

    # Get date of RSS entry, if possible
    try:
        temp = entry.updated_parsed
    except AttributeError:
        # Only the Arxiv feed is known not to give updated_parsed values (ie, dates for each entry).
        # Since the Arxiv RSS is refreshed daily anyway, we will assume these entries are new (except on weekends).
        isArxiv = True
    if isArxiv:
        isWeekday = dt.datetime.today().weekday() < 5
        isJustAnUpdate = entry.title[-8:-1] == "UPDATED"
        isNew = isWeekday and not isJustAnUpdate
    else:
        pubDate = int('%04d%02d%02d' % tuple(temp[0:3]))
        isNew = pubDate >= latestExecutionDate

    if getVeryInterestingEntries:
        return isVeryInteresting and isNew
    else:
        return isInteresting and isNew


def strip_html(text):
    return re.sub('<[^<]+?>', '', text)


def unicodeToAscii(uStr):
    # Strip accents etc. so the email body is plain ASCII (e.g. "Schrödinger" -> "Schrodinger").
    return normalize('NFKD', uStr).encode('ascii', 'ignore').decode('ascii')


def executiveSummary(feedURL, feedNameString, latestExecutionDate, listOfArxivIDsSoFar, getVeryInterestingEntries):
    print("Now checking: " + feedNameString)
    feed = feedparser.parse(feedURL)

    filtered_entries = [entry for entry in feed.entries if passes_filter(entry, latestExecutionDate, getVeryInterestingEntries)]
    if len(filtered_entries) == 0:
        return ('', 0, listOfArxivIDsSoFar)

    if 'ARXIV' in feedNameString.upper():
        ## Remove duplicate entries (eg, entries listed in both Q. Phys. and Cond.Mat.):
        dexesOfDuplicates = []
        for FEdex, entry in enumerate(filtered_entries):
            thisTitle = strip_html(entry.title)
            idStrStartDex = thisTitle.find('(arXiv:') + len('(arXiv:')
            idStrStopDex = thisTitle.find(' ', idStrStartDex)
            thisArxivID = thisTitle[idStrStartDex:idStrStopDex]
            if thisArxivID in listOfArxivIDsSoFar:
                dexesOfDuplicates.append(FEdex)
            else:
                listOfArxivIDsSoFar.append(thisArxivID)
        filtered_entries = [v for i, v in enumerate(filtered_entries) if i not in dexesOfDuplicates]

    numFilteredEntries = len(filtered_entries)
    if numFilteredEntries == 0:
        return ('', 0, listOfArxivIDsSoFar)

    ## Assemble the large summary string:
    largestring = "--------------- " + feedNameString + " ---------------"
    largestring = largestring + "\n"

    for entry in filtered_entries:
        try:
            largestring += "\n" + strip_html(entry.title) + "\n \n \t" + strip_html(entry.author) + "\n \t" + entry.link + "\n \n" + strip_html(entry.description) + "\n"
        except AttributeError:
            try:
                largestring += "\n" + strip_html(entry.title) + "\n \n \t" + entry.link + "\n \n" + strip_html(entry.description) + "\n"
            except AttributeError:
                pass

    return (unicodeToAscii(largestring), numFilteredEntries, listOfArxivIDsSoFar)


def sendSummaryEmails(recipientList, message, numVIentries, numOtherEntries):

    sender = 'sender@example.com'

    username = 'example@gmail.com'  # for gmail include "@gmail.com"
    powned = '******'  # thePwfor your account
    s = smtplib.SMTP('example.com', 587)

    s.ehlo()
    s.starttls()
    s.login(username, powned)

    subject = "cQED Digest " + time.strftime("%m/%d/%Y") + " [" + str(numVIentries) + "," + str(numOtherEntries) + "]"

    for recipient in recipientList:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        s.sendmail(sender, [recipient], msg.as_string())

    s.quit()
