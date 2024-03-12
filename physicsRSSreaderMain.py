#!/usr/bin/env python


# Revision: January 19, 2022

from subprocess import call

from functionDefs import executiveSummary, sendSummaryEmails

from recipients import recipientsList

import time

import sys
#from unicodedata import normalize



with open('latestRunDateTime','r') as f:

	latestExecutionDate = int(f.read())


# latestExecutionDate = 20220207
print latestExecutionDate



feedURLsAndNames=[
['Science Express','http://www.sciencemag.org/rss/express.xml'],

['Science Mag','http://www.sciencemag.org/rss/current.xml'],
['Nature AOP', 'http://feeds.nature.com/nature/rss/aop'],

['Nature','http://feeds.nature.com/nature/rss/current'],

['Nat. Phys. AOP','http://feeds.nature.com/nphys/rss/aop'],
['Nature Physics','http://feeds.nature.com/nphys/rss/current'],

['PRX','http://feeds.aps.org/rss/recent/prx.xml'],

['PRL','http://feeds.aps.org/rss/recent/prl.xml'],

['PRB','http://feeds.aps.org/rss/recent/prb.xml'],

['APL','http://scitation.aip.org/rss/content/aip/journal/apl/latestarticles?fmt=rss'],

['Phys Rev Applied','http://feeds.aps.org/rss/recent/prapplied.xml'],

['Nature Comm.','http://feeds.nature.com/ncomms/rss/current'],

['Science Advances','http://advances.sciencemag.org/rss/current.xml'],

['NJP','http://iopscience.iop.org/1367-2630/?rss=1'],

['Arxiv: Quant-Ph','http://arxiv.org/rss/quant-ph'],

['Arxiv: Cond-Mat','http://export.arxiv.org/rss/cond-mat']

]



dateOfExecution = time.strftime('%Y%m%d')

if int(dateOfExecution) == latestExecutionDate:
	sys.exit()

with open('latestRunDateTime', 'w') as f:

	f.write(dateOfExecution)



summariesAndLengths = []
VIsummariesAndLengths = []
listOfArxivIDsSoFar = [] # For use removing duplicate Arxiv entries (eg, listed as both cond-mat and quant-phys)

#Get summary of very interesting entries only
for feedInfo in feedURLsAndNames:
    result = executiveSummary(feedInfo[1],feedInfo[0],latestExecutionDate,listOfArxivIDsSoFar,True)
    #print result[-1]
    listOfArxivIDsSoFar += result[-1]
    VIsummariesAndLengths.append(result[:-1])

VIsummaries=[summary for [summary,numEntries] in VIsummariesAndLengths]
numVIEntriesList=[numEntries for [summary,numEntries] in VIsummariesAndLengths]
numVIEntriesTotal=sum(numVIEntriesList)

#Get summary of moderately interesting entries only
for feedInfo in feedURLsAndNames:
    result = executiveSummary(feedInfo[1],feedInfo[0],latestExecutionDate,listOfArxivIDsSoFar,False)
    listOfArxivIDsSoFar += result[-1]
    summariesAndLengths.append(result[:-1])

summaries=[summary for [summary,numEntries] in summariesAndLengths]
numEntriesList=[numEntries for [summary,numEntries] in summariesAndLengths]
numOtherEntriesTotal=sum(numEntriesList)


#summaries should have all been converted to ASCII by this point
while '' in VIsummaries: VIsummaries.remove('')
while '' in summaries: summaries.remove('')

numVISummaries=len(VIsummaries) # number of "very interesting" (author match) summaries
numSummaries=len(summaries) # number of "interesting" (keyword match) summaries


if numVISummaries + numSummaries >= 1:
	summarySum = "Select publications from "+str(latestExecutionDate)+" to "+str(dateOfExecution)+":\n\n"
	summarySum += "-~-PROBABLY OF INTEREST (author matches)-~-\n\n"
	summarySum += "\n".join(VIsummaries)
        summarySum += "\n"
	summarySum += "-~-~-~-POSSIBLY OF INTEREST (keyword matches)-~-~-~-\n\n"
	summarySum += "\n".join(summaries)

	# summarySum += "\n \n" + "Want off this list? Send your request to aeddins@berkeley.edu. (Or just block the address cqedRSSscraper@gmail.com)."

	print(summarySum)
	with open('rssReaderLog','w') as f:
		f.write('\n\n\n\n\n')
		f.write(dateOfExecution)
		f.write(summarySum)

	sendSummaryEmails(recipientsList,summarySum,numVIEntriesTotal,numOtherEntriesTotal)
else:
	with open('rssReaderLog','w') as f:
		f.write('\n\n\n\n\n')
		f.write(dateOfExecution)
		f.write("no new publications found.")
	print "no new publications found."
















