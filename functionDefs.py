## Function definitions for the physics RSS feed reader.
from keywords import *
import re
import feedparser
#from subprocess import call
import smtplib # Import smtplib for the actual sending function
import time
import datetime as dt
from email.mime.text import MIMEText # Import the email modules we'll need
from unicodedata import normalize

def makeUnicode(input):
    if type(input) != unicode:
        input =  input.decode('utf-8','ignore')
        return input
    else:
        return input

def myFormat(text):
    #Remove punctuation, capitalization for checking for matches to keywords.
    return(re.sub(r'[^\w\s]','',text.lower()))

cleanr = re.compile('<.*?>')

def myAuthorFormat(text):
    if text in ['',u'',u'  ']:
        return('')
    #Remove punctuation, capitalization for checking for matches to keywords.
    text = text.replace('.', ' ')#sometimes initials aren't separated by spaces in listings
    text = text.replace('  ',' ')#remove any double spaces created by previous line
    formatted = re.sub(r'[^\w\s]','',text.lower())
    formatted = formatted.strip()
    nameList = formatted.split(' ')
    firstInitLastNameOnly = ''
    try:
        firstInitLastNameOnly = nameList[0][0] + ' '+nameList[-1]
    except:
        pass
    return(firstInitLastNameOnly)


def passes_filter(entry,latestExecutionDate, getVeryInterestingEntries):
    
    #Get author names from RSS entry, if possible... turns out the general case is not well defined and thus hard to handle!
    try:
        entryAuthors = entry.authors #this line may throw an attribute error
        #print "debug: entryAuthors = ", entryAuthors
        #print entryAuthors[0]

        if {} in entryAuthors:
            #print "debug 1"
            raise AttributeError('') #or the attribute in the RSS entry just may not contain the right info
    except AttributeError:
        try:
            entryAuthors = entry.author
        except AttributeError:
            #print "debug 2"
            entryAuthors = [""]
    if isinstance(entryAuthors,str) or isinstance(entryAuthors,unicode):
        entryAuthors = [entryAuthors]
    entryAuthors2 = []
    for entryAuthor in entryAuthors:
        # print entryAuthor
        try:
            entryAuthor = entryAuthor['name']
        except:
            pass
        entryAuthor = re.sub(cleanr,'',entryAuthor) #strips html tags
        entryAuthors2.extend(entryAuthor.split(',')) #break author lists apart by commas as needed, hopefully
    entryAuthors2 = [myAuthorFormat(entryAuthor) for entryAuthor in entryAuthors2]

    isVeryInteresting = any([myAuthorFormat(author) in entryAuthors2 for author in authors])
    if isVeryInteresting:
        isInteresting = False #helps avoid duplicates listings in the summary produced.
    else:
        isInteresting = (any([myFormat(word) in myFormat(entry.summary) for word in wordlist]) or any([myFormat(titleword) in myFormat(entry.title) for titleword in titlelist]))

    #debugging:
#    if isVeryInteresting or isInteresting:
#        print "Very interesting =",isVeryInteresting
#        print [author for author in entryAuthors]
#        print [myFormat(author) for author in entryAuthors]
    
    isArxiv=False
    
    #Get date of RSS entry, if possible
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
        [yearStr,monStr,dayStr] = [str(num) for num in temp[0:3]]
        if len(dayStr) == 1:
            dayStr = '0'+dayStr
        if len(monStr) == 1:
            monStr = '0'+monStr
        pubDate = int(yearStr+monStr+dayStr)
        isNew = pubDate >= latestExecutionDate
    #if not isNew:
        #print "debug -- not new:"
        #print pubDate
    if getVeryInterestingEntries:
        return(isVeryInteresting and isNew)
    else:
        return(isInteresting and isNew)

def strip_html(text):
    return re.sub('<[^<]+?>', '', text)

def unicodeToAscii(uStr):
	try:
		#print "debug: just encoded in ascii..."
		return(normalize('NFKD',uStr).encode('ascii','ignore'))
	except Exception as e1:
		#print "error1: "+str(e1)
		try:
			#print "debug: just ran str()"
			return(str(uStr))
		except Exception as e2:
			#print "error2: "+str(e2)
			#print "giving up unicode to ascii conversion"
			#print type(uStr)
			return(uStr)


def executiveSummary(feedURL,feedNameString,latestExecutionDate,listOfArxivIDsSoFar,getVeryInterestingEntries):
    print "Now checking: "+feedNameString
    feed = feedparser.parse(feedURL)

    filtered_entries = [entry for entry in feed.entries if passes_filter(entry,latestExecutionDate, getVeryInterestingEntries)]
    #print "filtered entries:"
    #print filtered_entries
    numFilteredEntriesWithDuplicates = len(filtered_entries)
    if numFilteredEntriesWithDuplicates == 0:
        return('',0,listOfArxivIDsSoFar)

    if 'ARXIV' in feedNameString.upper():
        ## Remove duplicate entries (eg, entries listed in both Q. Phys. and Cond.Mat.):
        FEdex=0
        dexesOfDuplicates=[]
        for entry in filtered_entries:
            thisTitle = strip_html(entry.title)
            idStrStartDex = thisTitle.find('(arXiv:') + len('(arXiv:')
            idStrStopDex = thisTitle.find(' ', idStrStartDex)
            thisArxivID = thisTitle[idStrStartDex:idStrStopDex]
            if thisArxivID in listOfArxivIDsSoFar:
                dexesOfDuplicates.append(FEdex)
            else:
                listOfArxivIDsSoFar.append(thisArxivID)
            FEdex += 1
        filtered_entries = [v for i, v in enumerate(filtered_entries) if i not in dexesOfDuplicates]

    numFilteredEntries = len(filtered_entries)
    if numFilteredEntries == 0:
        return('',0,listOfArxivIDsSoFar)

    ## Assemble the large summary string:
    largestring = "--------------- "+feedNameString+" ---------------"
    largestring = largestring+"\n"

    for entry in filtered_entries:
        try:
            largestring += "\n" + strip_html(entry.title) + "\n \n \t" + strip_html(entry.author) + "\n \t" + entry.link + "\n \n" + strip_html(entry.description) + "\n"
        except AttributeError:
            try:
                largestring += "\n" + strip_html(entry.title) + "\n \n \t" + entry.link + "\n \n" + strip_html(entry.description) + "\n"
            except AttributeError:
                pass

    return(unicodeToAscii(largestring),numFilteredEntries,listOfArxivIDsSoFar)

def sendSummaryEmails(recipientList,message,numVIentries,numOtherEntries):

    sender = 'sender@example.com'

    username = 'example@gmail.com'  # for gmail include "@gmail.com"
    powned = '******'  # thePwfor your account
    s = smtplib.SMTP('example.com:587')

    s.ehlo()
    s.starttls()
    s.login(username,powned)
	
#	msg['Subject'] = "cQED Digest "+str(time.strftime("%m/%d/%Y"))+" ["+str(numVIentries)+","+str(numOtherEntries)+"]"
#	msg['From'] = sender
#	#msg['To'] = ""   #", ".join(recipientList)
#	s.sendmail(sender, recipientList, msg.as_string())

    for recipient in recipientList:
        msg = MIMEText(message.encode('utf-8'))
        msg['Subject'] = "cQED Digest "+str(time.strftime("%m/%d/%Y"))+" ["+str(numVIentries)+","+str(numOtherEntries)+"]"
        msg['From'] = sender
        msg['To'] = recipient
        s.sendmail(sender, [recipient], msg.as_string())

    s.quit()

