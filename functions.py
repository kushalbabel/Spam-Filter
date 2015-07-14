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