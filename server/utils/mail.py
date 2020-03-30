import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail( subject, content ):
	# Server config
	port = 587  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "thegizbob@gmail.com"  # Enter your address
	receiver_email = "contact@commissionmedicale.fr"  # Enter receiver address
	password = "***"

	# Email content
	subject = subject
	body = content

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