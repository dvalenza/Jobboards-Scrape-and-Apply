##########################################
#Craigslist / Monster / Indeed  J0bScanner
#
#Scans craigslist, and monster.com for jobs, then 
#attempts to apply to job found
#
#By David Valenza
#
#For educational purposes only.

import re
import urllib
import urllib2
import os,sys
from bs4 import BeautifulSoup
import time
from subprocess import call

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

import password

#comment these to open browser
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

gmail_user = "davidvalenza@gmail.com"
gmail_pwd = password.pw

sleeptime = 3600 #one day worth of seconds.

keyword = ['entry']

locations_accepted=["Boston, MA","Cambridge, MA","Somerville, MA","Medford, MA","Everett, MA","Malden, MA","Arlington, MA","Boston","Cambridge","Somerville","Medford","Everett","Malden","Arlington"]


message = "Hi, I am very interested in the job available, please review my attached resume.\n\nThank you,\nDavid Valenza\nDavidValenza@gmail.com\n(978)809-6319\n\n"
resume = "DavidAValenza-Resume.docx"


links_cl = {'CL-Technical Support' : "http://boston.craigslist.org/search/tch",
            'CL-Software / DBA' : "http://boston.craigslist.org/search/sof"
            }
links_monster = {
                 'Monster-\"tech support, entry\" 02155' : "http://jobsearch.monster.com/search/tech-support_5?q=entry&where=02155__2C-Medford__2C-MA",
                 'Monster-\"developer, entry\" 02155' : "http://jobsearch.monster.com/search/developer_5?q=entry&where=02155__2C-Medford__2C-MA",
                 }
links_indeed = {
    'Indeed-\"entry\",\"developer\",\"02155\"':"http://www.indeed.com/jobs?q=entry+developer&l=02155",
}

total = 0
skipped = 0
emails_sent=0
failed = 0
failedstring = ""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def blue(self, string):
        return self.OKBLUE + string + self.ENDC

def mail(to, subject, text, attach):
   print "[+] Sending email to " + to 
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
         'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def email_grabber(target_url):
    htmlFile = urllib.urlopen(target_url)
    html = htmlFile.read()
    regexp_email = r'[\w\.-]+@[\w\.-]+';
    pattern = re.compile(regexp_email)
    emailAddresses = re.findall(pattern, html)
    return emailAddresses[0]#only first email found returned

def findCL_emails(link):
    print "[*] Finding Emails."
    email = ""
    driver = webdriver.Firefox()
    driver.get(link)
    try:
        #print "[*] Trying to detect recaptcha presence."
        time.sleep(5)
        #try:
        #    driver.find_elements("rc-anchor-center-container")
        #    
        #try: 
        #    driver.find_elements("lbbg")    
        #    print "[!] Recaptcha detected! Quitting all further scans!"
        #    failed +=1
        #    return 0
        #What we call the "runaround":
        driver.find_element_by_class_name('reply_button').click()#.send_keys(Keys.RETURN)
        time.sleep(5)
        #driver.find_element_by_class_name('mailapp')
        #This works....RE LOOK AT THIS KEY SEQUENCE, worked previously
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.SHIFT).key_down(Keys.TAB).key_up(Keys.TAB).key_down(Keys.TAB).perform()
        element = driver.switch_to.active_element
        email = element.text
        return email
    except: #no reply button found
        print "[!] No reply button, scanning text."
        global failedstring
        failedstring+="[!] No reply button, scanning text.s"
        return email
    finally:    
        driver.quit()
        if email != "":
            print "[+] Email found: " + email 
        else:
            print  "[-] No emails found."
            global failedstring
            failedstring += "[-] No emails found."
            global failed
            failed +=1

def scanCL(link):
  subtotal = 0 
  page = urllib2.urlopen(link).read()
  soup = BeautifulSoup(page)
  data = soup.findAll("a")
  location = soup.findAll('span', attrs={ 'class':'pnr'})
  skip = False
  for x in range (19,118): #main links start at 19th 'a' into html
    if skip == True:
        skip = False
        continue
    matchObj = re.search( r'(.*)'+ keyword[0] +'(.*?).*', str(data[x]) ,re.M|re.I)
    #print "data="+str(data[x])
    #print "keyword="+keyword[0]
    if matchObj:
         #print "in"
         try: 
             locationx = location[(x-19)/4].findAll("small")[0].string #Must divide index by 4 since main link is every 4 'a's
         except IndexError:
           locationx = ""
         for locations in locations_accepted:
             matchObj = re.search( r'(.*)'+ locations +'(.*?).*', locationx ,re.M|re.I)
             if matchObj:
                 #print "[+] Location Match!" #Debug printline
                 try:
                     link="http://boston.craigslist.org" + data[x]['href']
                     title = data[x].contents.pop()
                     string = bcolors.WARNING+"[+] " + str(locationx) +bcolors.ENDC+" "+ bcolors.OKBLUE + title  + bcolors.ENDC +" | "+link
                     try:
                         f = open("jobsfound.py","a+")
                         for line in f:
                             if (line.strip("\n") == title):
                                 print "[!] Duplicate found, skipping."
                                 global skipped
                                 skipped += 1
                                 skip = True
                                 break
                     except IOError:
                         print "No data file found! Creating one now."
                     if skip == False:
                         global total
                         total +=1
                         subtotal+=1
                         print string
                         f.write(title+"\n")
                         f.close()
                         email = findCL_emails(link)
                         if email != "":
                             if email == "x prohibited":
                                 global failedstring
                                 failedstring += "x prohibited found"
                                 global failed
                                 failed +=1
                                 break
                             else:
                                 global emails_sent
                                 emails_sent+=1
                                 #print email
                                 time.sleep(20)
                                 mail("davidvalenza@gmail.com", 
                                      "Applied to (Craigslist): "+title,  
                                      "Sent to: "+email+"\nLink: "+link+"\n--------------------------------\n"+message, 
                                      "jobsfound.py")
                                 mail(email,title, message, resume)
                 except IndexError:
                     continue
  if subtotal >= 1:       
      return bcolors.BOLD + "[*] " + str(subtotal) + " Results found" + bcolors.ENDC   
  else:
      print bcolors.FAIL + "[-] No Results.." + bcolors.ENDC 


                   
def applyMON(link):
    print "[*] Attempting to apply to job"
    driver = webdriver.Firefox()
    driver.get(link)
    try:
        driver.find_element_by_class_name('applyButtonTextStyle').click()
        try:
            try: 
                driver.find_element_by_id('tbxSgnEmail').send_keys("davidvalenza@gmail.com")
                driver.find_element_by_id('tbxSgnPassword').send_keys(password.pw)
                driver.find_element_by_id('tbxSgnPassword').send_keys(Keys.RETURN)
            except:
                pass
            time.sleep(5)
            try:
                driver.find_element_by_id('ethn_1').send_keys(Keys.SPACE)
            except:
                pass
            driver.find_element_by_id('btnSubmit').send_keys(Keys.RETURN)
            time.sleep(5)#not necessary, for viewing screen after submit 
        except:
            print "[-] Error finding submit button!"
            global failedstring
            failedstring+="[-] Error finding submit button!"
            global failed
            failed +=1
            return False
    except: #No button found?
        print "[-] Error finding apply button!"
        global failed
        failed +=1
        return False
        
        pass
    finally:
        driver.quit()
        pass

def scanMON(link):
    index = 0
    subtotal = 0
    page = urllib2.urlopen(link).read()
    soup = BeautifulSoup(page)

    tbody = soup.findAll('tbody')
    for tr in tbody[0].findAll('tr'):
        data = tr.findAll('div',attrs={'class':'jobTitleContainer'})
        locations  = tr.findAll('div',attrs={'class':'jobLocationSingleLine'})
        for div in data:
            links = div.findAll('a')
            matchObj = re.search( r'(.*)'+ str(keyword[0]) +'(.*?).*', str(links[0].contents) ,re.M|re.I)
            if matchObj:
                for location in locations_accepted:
                    try:
                        loc = str(locations[0].a.contents.pop())
                        matchObj2 = re.search( r'(.*)'+ location +'(.*?).*', loc ,re.M|re.I)
                        if matchObj2:
                            link = data[0].a['href']
                            locx = matchObj2.group()
                            title = str(data[0].a.contents.pop())
                            skip = False
                            try:
                                f = open("jobsfound.py","a+")
                                for line in f:
                                    if (line.strip("\n") == title):
                                        print "[!] Duplicate found, skipping."
                                        global skipped
                                        skipped += 1
                                        skip = True
                                        break
                            except IOError:
                                print "No data file found! Creating one now."
                                
                            if skip == False:
                                string = bcolors.OKBLUE +"[+] " + bcolors.ENDC + bcolors.WARNING+ locx +" "+bcolors.ENDC
                                string += bcolors.OKBLUE + title + bcolors.ENDC +" | " + link
                                print string
                                if applyMON(link) != False:
                                    f.write(title+"\n")
                                    f.close()
                                    mail("davidvalenza@gmail.com",  
                                         "Applied to (Monster): "+title,  
                                         "Link: "+link, 
                                         "jobsfound.py")
                                    subtotal+=1
                                    global total
                                    total +=1
                    except IndexError:
                        pass
                else:
                    continue
        index+=1

    if subtotal >= 1:       
        print bcolors.BOLD + "[+] " + str(subtotal) + " Results found" + bcolors.ENDC   
    else:
        print bcolors.FAIL + "[-] No Results.." + bcolors.ENDC 

def scanIndeed(link):
    #Why didnt i write the whole prog like this:  ......
    soup=BeautifulSoup(str(BeautifulSoup(urllib2.urlopen(link).read())(id="resultsCol")))("div", attrs={'class':' row result'})
    i=0
    for row in soup:
        for location in locations_accepted:
            loc = row('span',attrs={'itemprop':'addressLocality'})[0].contents
            #print loc[0]
            matchObj = re.search( r'(.*)'+ loc[0] +'(.*?).*', location ,re.M|re.I)
            if matchObj:
                title=""
                for word in row("a", attrs={'itemprop':'title'})[0].contents:
                    title+=str(word).strip("</b>")
                href="http://www.indeed.com"+row("a", attrs={'itemprop':'title'})[0]['href']
                print loc[0] + " | " + title +" | "+href
                i+=1
################################################################
def main():
    print bcolors.HEADER + "--Running jobfinder--" + bcolors.ENDC
    print bcolors.HEADER + "[*] Scanning Craigslist" + bcolors.ENDC 
    runOnce = False
    for key, value in links_cl.iteritems():
        for query in keyword:
            if runOnce == True:
                break
            link = value+"?query="+str(keyword[0])
            print  bcolors.HEADER + "[*] Scanning: " + key +" Keyword: "+query+" Link: "+link+bcolors.ENDC 
            scanCL(link)
            #runOnce = True #debug

    print  bcolors.HEADER + "[*] Scanning Monster" + bcolors.ENDC 
    for key, value in links_monster.iteritems():
        print  bcolors.HEADER +"[*] Scanning: " + key + bcolors.ENDC 
        scanMON(value)

    print  bcolors.HEADER + "[*] Scanning Indeed" + bcolors.ENDC 
    for key, value in links_indeed.iteritems():
        print  bcolors.HEADER +"[*] Scanning: " + key + bcolors.ENDC 
        scanIndeed(value)
    
if __name__ == "__main__":
  x = True
  while x:
    x=False #run once (usefull for non cronjob)
    counter = 1 
    if len(sys.argv)>1:
        print "Usage: python jobfinder.py"
        exit()
    try:
            #call(["clear"])
        main()
        call(["date"])
        global failed
        print bcolors.OKGREEN + "[+] Total failed: " + str(failed) + bcolors.ENDC
        print bcolors.OKGREEN + "[+] Total emails sent: " + str(emails_sent) + bcolors.ENDC
        print bcolors.OKGREEN + "[+] Total skipped: " + str(skipped) + bcolors.ENDC
        if total == 0:
            print "[*] No new results found."
        else:
            print bcolors.OKGREEN + "[+] Total found: " + str(total) + bcolors.ENDC
        if x:
            print bcolors.WARNING +"[+] "+str(counter)+" scan finished, sleeping " + str(((sleeptime/60)/60)) + " hours.." +bcolors.ENDC
    
        #Not necessary with cronjob
        #if total > 0:
        #    mail("davidvalenza@gmail.com",  
        #         "Jobsfound Summary",  
        #         "[+] Total failed: "+str(failed)+"\n[+] Total emails sent: "+str(emails_sent)+"\n[+] Total skipped: "+str(skipped)+"\n[+] Total found: "+str(total),
        #         "jobsfound.py")
	if x:
          time.sleep(sleeptime)
    except KeyboardInterrupt:
        print('\n\n[!] Keyboard exception received. Exiting.')
        exit()
