#!/usr/bin/env python3

# Revision: November 16, 2026 (ported to Python 3)

import argparse
import datetime as dt
import sys
import time

from functionDefs import executiveSummary, feedProblem, sendSummaryEmails, buildEmail, plainText
from recipients import loadRecipients

parser = argparse.ArgumentParser(description='Physics RSS digest. With no options: normal daily run.')
parser.add_argument('--test', metavar='EMAIL',
                    help='send the digest only to EMAIL; does not read or update latestRunDateTime')
parser.add_argument('--test-all', action='store_true',
                    help='send the digest to everyone in recipients.txt as a trial: '
                         'does not read or update latestRunDateTime')
parser.add_argument('--preview', metavar='FILE.eml',
                    help='write the email to FILE.eml (open it in Outlook/Thunderbird) instead of sending; '
                         'does not update latestRunDateTime')
parser.add_argument('--since', metavar='YYYYMMDD', type=int,
                    help='include papers from this date on (default: last run date; '
                         'with --test/--test-all/--preview: 3 days ago)')
args = parser.parse_args()
# Abstracts contain Greek letters etc.; don't let a non-UTF-8 console or log redirect crash the run.
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
isTrialRun = bool(args.test or args.test_all or args.preview)
# Load the recipient list up front so a missing recipients.txt stops the run before anything else happens.
recipientsList = None if (args.test or args.preview) else loadRecipients()

if args.since:
    latestExecutionDate = args.since
elif isTrialRun:
    latestExecutionDate = int((dt.date.today() - dt.timedelta(days=3)).strftime('%Y%m%d'))
else:
    with open('latestRunDateTime', 'r') as f:
        latestExecutionDate = int(f.read())

print(latestExecutionDate)


# Order matters for duplicates: a paper is listed under the first feed it appears in, so each
# journal's main feed (which has author names) comes before its subject feeds (titles only).
feedURLsAndNames = [
    # APS
    ['PRL', 'https://feeds.aps.org/rss/recent/prl.xml'],
    ['PRX', 'https://feeds.aps.org/rss/recent/prx.xml'],
    ['PRX Quantum', 'https://feeds.aps.org/rss/recent/prxquantum.xml'],
    ['PRA', 'https://feeds.aps.org/rss/recent/pra.xml'],
    ['Phys. Rev. Applied', 'https://feeds.aps.org/rss/recent/prapplied.xml'],
    ['Phys. Rev. Research', 'https://feeds.aps.org/rss/recent/prresearch.xml'],
    ['PRB', 'https://feeds.aps.org/rss/recent/prb.xml'],

    # Nature family. The main feeds only carry the ~8 newest items, so the subject feeds
    # (titles only, no authors or abstracts) fill in the papers that scroll off.
    ['Nature', 'https://www.nature.com/nature.rss'],
    ['Nature Physics', 'https://www.nature.com/nphys.rss'],
    ['Nature Physics (quantum physics subject)', 'https://www.nature.com/subjects/quantum-physics/nphys.rss'],
    ['Nature Comm.', 'https://www.nature.com/ncomms.rss'],
    ['Nature Comm. (physics subject)', 'https://www.nature.com/subjects/physics/ncomms.rss'],
    ['Nature Comm. (quantum information subject)', 'https://www.nature.com/subjects/quantum-information/ncomms.rss'],
    ['npj Quantum Information', 'https://www.nature.com/npjqi.rss'],

    # Science
    ['Science', 'https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science'],
    ['Science First Release', 'https://www.science.org/action/showFeed?type=axatoc&feed=rss&jc=science'],
    ['Science Advances', 'https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=sciadv'],

    # Others
    ['Quantum', 'https://quantum-journal.org/feed/'],
    ['NJP', 'https://iopscience.iop.org/journal/rss/1367-2630'],
    ['APL', 'https://pubs.aip.org/rss/site_1000017/1000011.xml'],  # current issue; no author names in this feed

    # arXiv
    ['Arxiv: Quant-Ph', 'https://rss.arxiv.org/rss/quant-ph'],
    ['Arxiv: Cond-Mat', 'https://rss.arxiv.org/rss/cond-mat'],
    ['Arxiv: Hep-Ex', 'https://rss.arxiv.org/rss/hep-ex'],  # axion / dark-matter searches (ADMX etc.)
    ['Arxiv: Physics.Ins-Det', 'https://rss.arxiv.org/rss/physics.ins-det'],  # detectors, haloscopes, sensors
]


dateOfExecution = time.strftime('%Y%m%d')

if not isTrialRun:
    if int(dateOfExecution) == latestExecutionDate:
        sys.exit()
    with open('latestRunDateTime', 'w') as f:
        f.write(dateOfExecution)


seenPaperIDs = set()  # papers already listed (any feed, either pass); executiveSummary adds to it

# Get summary of very interesting entries only (author matches)
VIsummariesAndLengths = [executiveSummary(feedURL, feedName, latestExecutionDate, seenPaperIDs, True)
                         for feedName, feedURL in feedURLsAndNames]
VIsummaries = [summary for (summary, numEntries) in VIsummariesAndLengths if summary != '']
numVIEntriesTotal = sum(numEntries for (summary, numEntries) in VIsummariesAndLengths)

# Get summary of moderately interesting entries only (keyword matches)
summariesAndLengths = [executiveSummary(feedURL, feedName, latestExecutionDate, seenPaperIDs, False)
                       for feedName, feedURL in feedURLsAndNames]
summaries = [summary for (summary, numEntries) in summariesAndLengths if summary != '']
numOtherEntriesTotal = sum(numEntries for (summary, numEntries) in summariesAndLengths)

# Feeds that returned nothing usable (dead URL, server error, bot-check page, ...)
deadFeeds = [(feedName, feedProblem(feedURL)) for feedName, feedURL in feedURLsAndNames if feedProblem(feedURL)]
deadFeedWarning = ''
if deadFeeds:
    deadFeedWarning = ("\n\n*** WARNING: no data received from %d of %d feeds -- their URLs may need updating "
                       "(in physicsRSSreaderMain.py):\n" % (len(deadFeeds), len(feedURLsAndNames)))
    deadFeedWarning += "".join("    - %s: %s\n" % (name, problem) for name, problem in deadFeeds)
    print(deadFeedWarning)


if VIsummaries or summaries or deadFeeds:
    summarySum = "Select publications from " + str(latestExecutionDate) + " to " + str(dateOfExecution) + ":\n\n"
    if VIsummaries or summaries:
        summarySum += "-~-PROBABLY OF INTEREST (author matches)-~-\n\n"
        summarySum += "\n".join(VIsummaries)
        summarySum += "\n"
        summarySum += "-~-~-~-POSSIBLY OF INTEREST (keyword matches)-~-~-~-\n\n"
        summarySum += "\n".join(summaries)
    else:
        summarySum += "No new matching publications.\n"
    summarySum += deadFeedWarning

    # summarySum += "\n \n" + "Want off this list? Send your request to aeddins@berkeley.edu. (Or just block the address cqedRSSscraper@gmail.com)."

    print(plainText(summarySum))

    if args.preview:
        msg = buildEmail(summarySum, numVIEntriesTotal, numOtherEntriesTotal, 'physics-digest@preview', args.test or 'preview@preview')
        with open(args.preview, 'w', encoding='utf-8') as f:
            f.write(msg.as_string())
        print('Wrote preview to ' + args.preview)
    elif args.test or args.test_all:
        trialRecipients = [args.test] if args.test else recipientsList
        sendSummaryEmails(trialRecipients, summarySum, numVIEntriesTotal, numOtherEntriesTotal)
        print('Sent test digest to ' + ', '.join(trialRecipients))
    else:
        with open('rssReaderLog', 'w', encoding='utf-8') as f:
            f.write('\n\n\n\n\n')
            f.write(dateOfExecution)
            f.write(plainText(summarySum))
        sendSummaryEmails(recipientsList, summarySum, numVIEntriesTotal, numOtherEntriesTotal)
else:
    with open('rssReaderLog', 'w', encoding='utf-8') as f:
        f.write('\n\n\n\n\n')
        f.write(dateOfExecution)
        f.write("no new publications found.")
    print("no new publications found.")
