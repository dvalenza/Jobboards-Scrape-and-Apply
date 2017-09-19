  
Scans listings of craigslist and monster for jobs matching location and search term, then emails  
resume to job.  
  
Creates a log of jobs applied to prevent emailing same job twice.  
  
Usage: python jobfinder.py searchterm  
  
Example Output (only first 4 results):  
  
[*] Running scanner - Scanning for keyword: entry  
-----------------------------  
[*] >> Scanning Craigslist <<  
-----------------------------  
[*] Scanning: CL-Software / DBA  
[+]  (Boston, MA) Entry Level Javascript Developer/ Technical Consultant | http://boston.craigslist.org/gbs/sof/5069436934.html  
[*] Finding Emails.  
[+] Email found: 5xv67-5069436934@job.craigslist.org  
[+] Sending email to davidvalenza@gmail.com  
[+]  (Cambridge, MA) Data Entry for app needed ASAP | http://boston.craigslist.org/gbs/sof/5058178195.html  
[*] Finding Emails.  
[+] Email found: qfrm5-5058178195@job.craigslist.org  
[+] Sending email to davidvalenza@gmail.com  
[*] Scanning: CL-Technical Support  
[+]  (Boston, MA) IT Help Desk Specialist / Entry-Level Web Dev | http://boston.craigslist.org/gbs/tch/5052635731.html  
[*] Finding Emails.  
[+] Email found: brbhc-5052635731@job.craigslist.org  
[+] Sending email to davidvalenza@gmail.com  
[+]  (Boston, MA) Help Desk Specialist / Entry-Level Web Development | http://boston.craigslist.org/gbs/tch/5037116000.html  
[*] Finding Emails.  
[+] Email found: vvxzm-5037116000@job.craigslist.org  
[+] Sending email to davidvalenza@gmail.com  
---------------------------  
[+] >> Scanning Monster <<  
---------------------------  
[*] Scanning: Monster-"tech support" 02155  
[-] No Results..  
[*] Scanning: Monster-"tech support" "entry" 02155  
[+] Entry Level System Support/Helpdesk Analyst | http://jobview.monster.com:80/Entry-Level-System-Support-Helpdesk-Analyst-Job-North-Reading-MA-US-150922172.aspx?mescoid=1500134001001&jobPosition=6  
[+] Technical Support Engineer/Spec -Entry Level Opening | http://job-openings.monster.com:80/monster/c247dfdd-9f22-4eaa-9efd-b64bb0925a13?mescoid=1500134001001&jobPosition=15  
[+] Help Desk Specialist / Entry-Level Web Development | http://job-openings.monster.com:80/monster/576ce0c7-7093-438a-8f24-ce5949dfbcd1?mescoid=1500134001001&jobPosition=16  
[+] Help Desk Specialist / Entry-Level Web Development | http://job-openings.monster.com:80/monster/aae71d43-4e76-4b43-a231-232056958d58?mescoid=1500134001001&jobPosition=18  
[+] Technical Support Engineer/Rep-Entry Level Opportunity | http://job-openings.monster.com:80/monster/18d4333b-27b1-42bf-96eb-6ad41b376b67?mescoid=1500134001001&jobPosition=19  
[+] 5 Results found  
[*] Scanning: Monster-"developer" "entry" 02155  
[+] Software Engineer - entry level | http://jobview.monster.com:80/Software-Engineer-entry-level-Job-Wilmington-MA-US-147504876.aspx?mescoid=1500127001001&jobPosition=1  
[+] Entry Level C# .NET Programmers / Developers / Analysts | http://jobview.monster.com:80/Entry-Level-C-NET-Programmers-Developers-Analysts-Job-Andover-MA-US-149667106.aspx?mescoid=1500127001001&jobPosition=2  
[+] Entry Level Embedded Software Developer | http://jobview.monster.com:80/Entry-Level-Embedded-Software-Developer-Job-Needham-150950951.aspx?mescoid=1500128001001&jobPosition=10  
[+] Compiler Engineer (Entry Level) | http://jobview.monster.com:80/Compiler-Engineer-Entry-Level-Job-Natick-MA-US-151335353.aspx?mescoid=1500127001001&jobPosition=13  
[+] Entry Level Software Engineer / Robotics Engineer - Automation - Woburn, MA | http://job-openings.monster.com:80/monster/a49361f8-1b7d-4336-8060-3d371fde7e00?mescoid=1500127001001&jobPosition=15  
[+] 5 Results found  
[+] 1 scan finished, sleeping 30 minutes..  
[+] Total emails sent: 4  
[+] Total skipped: 0  
[+] Grand Total: 4  
  
  
