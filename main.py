import mechanize
from bs4 import BeautifulSoup
import re
import math

from functions import *
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
keywords.close()
keywords_list=open("keywords.txt").read().splitlines()

print "The blacklisted keywords are: "

print keywords_list


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
test=open("ScannedEmails.txt","wb")

mainPageSoup=BeautifulSoup(loggedinhtml)
all_frames = mainPageSoup.find_all('frame')

mainlink="http://iloha.iitb.ac.in/"+all_frames[3]['src']

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

#loop to check if each mail is spam or not
totalSpammed=0
for i in range(0,total_mails):

	email_link= all_emails[i]
	email_link="http://iloha.iitb.ac.in/"+email_link
	
	br.open(email_link)
	emaildata=br.response().read()
	email_subject= subject(emaildata)
	email_sender = sender(emaildata)
	email_to= to(emaildata)
	email_body=body(emaildata)
	
	test.write(str(i+1) +".  "+email_subject)
	test.write('\n')
	print (str(i+1) +".  "+email_subject)

	if decideSpam(email_subject,email_sender,email_to,email_body,keywords_list):
		br.select_form(nr=0)
		control=br.form.find_control('moveto')
		for item in control.items:
			if item.name=="INBOX.Spam":
				item.selected= True
				break
		br.submit()	
		totalSpammed+=1
		print "***************Spammed*****************"
	print '\n'	
print (str(totalSpammed)+" mail(s) moved to the Spam Folder!")
test.close()