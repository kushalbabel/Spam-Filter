import mechanize
from bs4 import BeautifulSoup
import re
import math

def subject(emaildata):
	start=emaildata.find("SUBJECT")
	start=emaildata.find("mainHeading",start)
	start=start+16
	end=emaildata.find("</b>",start)
	return emaildata[start:end]

def sender(emaildata):
	start=emaildata.find("From:  </b>")
	start=emaildata.find("target",start)
	start+=16
	end=emaildata.find("</a>",start)
	return emaildata[start:end]

def to(emaildata):
	start=emaildata.find("To: </b>")
	start=emaildata.find("target",start)
	start+=16
	end=emaildata.find("</a>",start)
	return emaildata[start:end]


def body(emaildata):
	start=emaildata.find("<!-- BEGIN")
	end=emaildata.find("<!-- END MESSAGE CELL //-->",start)
	end+=26
	return emaildata[start:end]
	

def decideSpam(email_subject,email_sender,email_to,email_body,keywords_list):
	'''black=["POWER SHUTDOWN","Lost & Found","IITB in News:","Library","PG","Electrical Maintenance",
			"Live Screening","Ph.D.","M.Tech.","hostel"]
	if any (phrase in email_subject for phrase in black ):
		return True
	else :
		return False'''
	
	found=False
	for line in keywords_list:
		
		if line in email_subject:
			found=True
			print (line,"Found!")
			break
		
	return found	
def email_table(maindata,all_emails,j,total_mails):
	end=0
	
	for i in range(15*j,min(15*(j+1),total_mails)):
		start=maindata.find("read_message",end)
		end=maindata.find('DESC',start)+4
		all_emails[i]=maindata[start:end]
		
	return all_emails
#getting keywords into a file.
keywords=open("keywords.txt","a+")
print "Enter the key words to be blacklisted, -1 to submit"
while True:
	keyword=raw_input()
	if keyword=='-1' :
		break
	else :
		keywords.write(keyword)
		keywords.write('\n')
keywords_list=keywords.read().splitlines()

total_mails=input("Enter the first few number of mails to be filtered: ")
all_emails=[None]*total_mails

br = mechanize.Browser()
br.open('http://iloha.iitb.ac.in/index.php')

userPrefs = open("preferences.txt").read().splitlines()

br.select_form(nr = 0)
br.form['user']= userPrefs[0]
br.form['password'] = userPrefs[1]
br.submit()

loggedinhtml= br.response().read()
#Logged In!
test=open("test.txt","wb")

mainPageSoup=BeautifulSoup(loggedinhtml)
all_frames = mainPageSoup.find_all('frame')

mainlink="http://iloha.iitb.ac.in/"+all_frames[3]['src']
print mainlink
br.open(mainlink)
maindata=br.response().read()
for j in range(0,int(math.ceil(total_mails/15.0))):

	email_table(maindata,all_emails,j,total_mails)
	br.select_form(nr=0)
	control=br.form.find_control('start')
	for item in control.items:
		if item.name==str(15*(j+1)):
			item.selected= True
			break
	maindata=br.submit().read()


print len(all_emails)
#loop to check if each mail is spam or not
for i in range(0,total_mails):

	email_link= all_emails[i]
	email_link="http://iloha.iitb.ac.in/"+email_link
	print email_link
	br.open(email_link)
	emaildata=br.response().read()
	email_subject= subject(emaildata)
	email_sender = sender(emaildata)
	email_to= to(emaildata)
	email_body=body(emaildata)
	
	test.write(email_subject)
	test.write('\n')
	print email_subject

	if decideSpam(email_subject,email_sender,email_to,email_body,keywords_list):
		br.select_form(nr=0)
		control=br.form.find_control('moveto')
		for item in control.items:
			if item.name=="INBOX.Spam":
				item.selected= True
				break
		br.submit()		
		print "***************Spammed*****************"
		
test.close()