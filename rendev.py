## coding=utf-8

# Time lib to sleep
import time	
import datetime
# importing the requests library 
import requests
from requests.exceptions import HTTPError

# Count number of request sent
nbRequestSent=0

while 1==1:
	f=open("output.txt", "a+")
	f.write("============ Wake Up 73kBot _o/ "+str(nbRequestSent)+" ============"+ "\r\n")
	f.close()
	nbRequestSent+=1

	# 3 months from now
	weeknumbers = ["0","7","14","21","28","35","42","49","56","63","70","77","84","91"]
	# weeknumbers = ["98"]
	for weeknumber in weeknumbers:

		now = datetime.datetime.now()
		f=open("output.txt", "a+")
		f.write("["+now.strftime("%H:%M") + "]Week starts "+weeknumber+" days from today"+ "\r\n")
		f.close()
		
		# api-endpoint 
		# weeknumber = "98" #2-8sept
		# weeknumber2 = "119" #23-29sept
		URL = "http://www.rdv.puy-de-dome.gouv.fr/ezjscore/call/bookingserver::planning::assign::801::809::" + weeknumber
		# URL2 = "http://www.rdv.puy-de-dome.gouv.fr/ezjscore/call/bookingserver::planning::assign::801::809::"+weeknumber2

		# fake header to bypass security
		headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

		# sending get request and saving the response as response object
		try:
			response = requests.get(URL, headers = headers)
			# If the response was successful, no Exception will be raised
			response.raise_for_status()
		except HTTPError as http_err:
			f=open("output.txt", "a+")
			f.write(f"HTTP error occurred: {http_err}"+ "\r\n")  # Python 3.6
			f.close()
			break
		except Exception as err:
			f=open("output.txt", "a+")
			f.write(f"Other error occurred: {err}"+ "\r\n")  # Python 3.6
			f.close()
			break
		else:
			# extracting data in raw text format
			# data = response.content
			data = response.text
			
			found1 = data.find('libre',0,(data.find('Légende'))) != -1

			# Send email when slot found
			if found1:
				f=open("output.txt", "a+")
				f.write("!!!!!!!!!!!!!!!!!!SLOT FOUND!!!!!!!!!!!!!!!!!!"+ "\r\n")
				f.write("!!!!!!!!!!!!!!!!!!SLOT FOUND!!!!!!!!!!!!!!!!!!"+ "\r\n")
				f.write("!!!!!!!!!!!!!!!!!!SLOT FOUND!!!!!!!!!!!!!!!!!!"+ "\r\n")
				f.write("!!!!!!!!!!!!!!!!!!SLOT FOUND!!!!!!!!!!!!!!!!!!"+ "\r\n")
				f.write("!!!!!!!!!!!!!!!!!!SLOT FOUND!!!!!!!!!!!!!!!!!!"+ "\r\n")
				f.close()
				import smtplib, ssl
				from email.mime.base import MIMEBase
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText

				# Server config
				port = 587  # For SSL
				smtp_server = "smtp.gmail.com"
				sender_email = "thegizbob@gmail.com"  # Enter your address
				receiver_email = "olivier.peyronnel@gmail.com"  # Enter receiver address
				password = "***"

				# Email content
				subject = "/!\\ Slot libre semaine "+weeknumber+" /!\\"
				body = "http://www.rdv.puy-de-dome.gouv.fr/booking/create/801/4"
				
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
					# Can be omitted
					server.ehlo()
					server.starttls()	
					server.ehlo()
					server.login(sender_email, password)
					server.sendmail(sender_email, receiver_email, text)
				except Exception as e:
				    # Print any error messages to stdout
				    f=open("output.txt", "a+")
				    f.write("Erreur: ",e)
				    f.write("\r\n")
				    f.close()
				    exit()
				finally:
					server.quit()
					f=open("output.txt", "a+")
					f.write("73kBot sent a mail to 73k05"+ "\r\n")
					f.close()

	# Sleeping time in minutes
	sleeptime = 1
	f=open("output.txt", "a+")
	f.write("============ 73kBot will sleep "+str(sleeptime)+" minutes _o/ "+str(nbRequestSent)+" ============"+ "\r\n")
	f.close()
	time.sleep(sleeptime*60)
