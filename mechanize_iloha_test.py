import mechanize
from bs4 import BeautifulSoup

def subject(soup):
	return soup.find_all('table')[3].get_text()

def sender(soup):
	return soup.find_all('table')[4].find_all('tr')[1].get_text()[:-4]

def to(soup):
	return soup.find_all('table')[4].find_all('tr')[2].get_text()[:-4]

def body(soup):
	return soup.find_all('table')[5]	

def decideSpam(email_subject,email_sender,email_to,email_body):
	black=["POWER SHUTDOWN","Lost & Found","IITB in News:","Library","PG","Electrical Maintenance",
			"Live Screening","Ph.D.","M.Tech.","[Student-notices]"]
	if any (word in email_subject for word in black):
		return True
	else :
		return False


br = mechanize.Browser()
br.open('http://iloha.iitb.ac.in/index.php')

userPrefs = open("preferences.txt").read().splitlines()

br.select_form(nr = 0)
br.form['user']= userPrefs[0]
br.form['password'] = userPrefs[1]
br.submit()

loggedinhtml= br.response().read()

test=open("test.html","wb")

mainPageSoup=BeautifulSoup(loggedinhtml)
all_frames = mainPageSoup.find_all('frame')

mainlink="http://iloha.iitb.ac.in/"+all_frames[3]['src']
print mainlink

br.open(mainlink)
maindata=br.response().read()
test.write(maindata)
test.close()

maindatasoup=BeautifulSoup(maindata)
email_table=maindatasoup.find_all('table')[2]
all_emails=email_table.find_all('tr')
print len(all_emails)
for i in range(1,16):

	email_link= all_emails[i].find_all('a')[0]['href']
	email_link="http://iloha.iitb.ac.in/"+email_link
	print email_link
	br.open(email_link)
	emaildatasoup=BeautifulSoup(br.response().read())
	email_subject= subject(emaildatasoup)
	email_sender = sender(emaildatasoup)
	email_to= to(emaildatasoup)
	email_body=body(emaildatasoup)
	print len(emaildatasoup.find_all('table'))
	print email_subject
	if decideSpam(email_subject,email_sender,email_to,email_body):
		br.select_form(nr=0)
		control=br.form.find_control('moveto')
		for item in control.items:
			if item.name=="INBOX.Spam":
				item.selected= True
				break
		br.submit()		
		print "***************Spammed*****************"
		