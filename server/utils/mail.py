import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def createBody(date_free_slot, booking):
    content = f"Bonjour {booking['firstname']},<br/><br/>"
    content += f"Nous avons trouvé un créneau pouvant t'interesser. "
    content += f"Rends toi au plus vite sur {booking['bookUrl']}, la date {date_free_slot} est disponible. "
    content += f"Nous avons enregistré cette date elle ne te sera plus proposée. Par contre si on trouve un créneau plus proche " \
               f"de la date que tu as choisi, on te renverra un email.<br/><br/>"
    content += f"Si tu es satisfait de nos services, on te propose de nous faire un don de 5euros ou plus sur https://www.helloasso.com/associations/commissionmedicale/formulaires/1<br/><br/>"
    content += f"Bonne conduite<br/>Bob"
    return content


def send_mail(subject, date_free_slot, booking):
    # Server config
    port = 587  # For SSL
    smtp_server = "mail34.lwspanel.com"
    sender_email = "booking@commissionmedicale.fr"  # Enter your address
    receiver_email = booking["email"]
    bcc = "contact@commissionmedicale.fr"
    password = "***"

    # Email content
    subject = subject
    body = createBody(date_free_slot, booking)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "Bob <" + sender_email + ">"
    message["To"] = receiver_email
    message["Bcc"] = bcc
    # message["Cc"] = bcc
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "html"))
    text = message.as_string()

    toaddrs = [receiver_email] + [bcc]

    # Send mail
    try:
        server = smtplib.SMTP(smtp_server, port)
        # Can be omitted
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, toaddrs, text)
    except Exception as e:
        # Print any error messages to stdout
        f = open("output.txt", "a+")
        f.write("Erreur: ", e)
        f.write("\r\n")
        f.close()
        exit()
    finally:
        server.quit()
        f = open("output.txt", "a+")
        f.write("73kBot sent a mail to 73k05" + "\r\n")
        f.close()
