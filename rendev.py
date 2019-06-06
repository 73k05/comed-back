## coding=utf-8

# Time lib to sleep
import time	
# importing the requests library 
import requests 	

while 1==1:
	print("Wake Up 73kBot _o/")
	  
	# api-endpoint 
	weeknumber = "98" #2-8sept
	# weeknumber2 = "119" #23-29sept
	URL = "http://www.rdv.puy-de-dome.gouv.fr/ezjscore/call/bookingserver::planning::assign::801::809::"+weeknumber
	# URL2 = "http://www.rdv.puy-de-dome.gouv.fr/ezjscore/call/bookingserver::planning::assign::801::809::"+weeknumber2

	# fake header to bypass security
	headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
	  
	# sending get request and saving the response as response object 
	print("Sending request...")
	r = requests.get(URL, headers = headers)
	# r2 = requests.get(URL2, headers = headers)
	  
	# extracting data in raw text format
	data = r.content
	# data2 = r2.content

	found1 = data.find('libre',0,(data.find('Légende'))) != -1
	# found2 = data2.find('libre',0,(data2.find('Légende'))) != -1

	# print(data)
	# print("Index of Legende: ",data.find('Légende'))
	print("Slot libre found: ",
		'Oui' if found1 else 'Non')
	# print("Slot libre 2 found: ",
	# 	'Oui' if found2 else 'Non')

	# Send email when slot found
	if found1:
		import smtplib, ssl
		from email.mime.base import MIMEBase
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText

		# Server config
		port = 587  # For SSL
		smtp_server = "smtp.gmail.com"
		sender_email = "thegizbob@gmail.com"  # Enter your address
		receiver_email = "gizmogrosbob8@hotmail.com"  # Enter receiver address
		password = "***"

		# Email content
		subject = "/!\\ Slot libre semaine "+weeknumber+" /!\\"
		body = "http://www.rdv.puy-de-dome.gouv.fr/booking/create/801"
		
		# Create a multipart message and set headers
		message = MIMEMultipart()
		message["From"] = "73kBot <"+sender_email+">"
		message["To"] = receiver_email
		message["Subject"] = subject

		# Add body to email
		message.attach(MIMEText(body, "plain"))
		text = message.as_string()

		# Send mail
		try:
		    server = smtplib.SMTP(smtp_server,port)
		    server.ehlo() # Can be omitted
		    server.starttls()	
		    server.ehlo()
		    server.login(sender_email, password)
		    server.sendmail(sender_email, receiver_email, text)
		except Exception as e:
		    # Print any error messages to stdout
		    print("Erreur: ",e)
		    exit()
		finally:
		    server.quit()

		print("73kBot sent a mail to 73k05")

	# Sleeping time in minutes
	sleeptime = 5
	print("73kBot will sleep "+str(sleeptime)+" minutes")
	time.sleep(sleeptime*60)
