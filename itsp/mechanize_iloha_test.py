import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.open('http://iloha.iitb.ac.in/index.php')
for form in br.forms():
     print form

userPrefs = open("preferences.txt").read().splitlines()

br.select_form(nr = 0)
br.form['user']= userPrefs[0]
br.form['password'] = userPrefs[1]
br.submit()
loggedinhtml= br.response().read()

print loggedinhtml
test=open("test.html","wb")

print '######################################'
#########################
####BeautifulSoup########
#########################



mainPageSoup=BeautifulSoup(loggedinhtml)
all_frames = mainPageSoup.find_all('frame')

for frame in all_frames:
	print frame
	print '#################################'

print all_frames[3]['src']

mainlink="http://iloha.iitb.ac.in/"+all_frames[3]['src']
print mainlink

br.open(mainlink)
maindata=br.response().read()

test.write(maindata)
test.close()

maindatasoup=BeautifulSoup(maindata)
all_tables=maindatasoup.find_all('table')

print "***************************************************************"

email_link= all_tables[2].find_all('tr')[2].find_all('a')[0]['href']
email_link="http://iloha.iitb.ac.in/"+email_link

print email_link

br.open(email_link)
emaidatasoup=BeautifulSoup(br.response().read())
print emaidatasoup.find_all('form')

br.select_form(nr=0)
control=br.form.find_control('moveto')

for item in control.items:
	if item.name=="INBOX.Spam":
		item.selected= True
		break

spammed=br.submit()