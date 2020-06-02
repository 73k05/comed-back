import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from log import write_log


def createBody(date_free_slot, booking):
    content = f"Bonjour {booking['firstname']},<br/><br/>"
    content += f"Merci d'avoir réservé sur <a href='https://www.commissionmedicale.fr'>CommissionMedicale</a>. Nous avons trouvé un créneau pouvant vous interesser. "
    content += f"Rendez vous au plus vite sur <a href={booking['bookUrl']}>gouv</a>, la date {date_free_slot.strftime('%d/%m/%Y')} est disponible. " \
               f"Si le créneau {date_free_slot.strftime('%d/%m/%Y')} n'est plus disponible, notre outil est déjà en train de chercher une meilleure date pour vous.<br/><br/>" \
               f"Dans le cas ou le créneau {date_free_slot.strftime('%d/%m/%Y')} est trop proche de la date de souhaitée, " \
               f"moins d'une semaine par exemple il sera difficile d'en trouver un mieux. " \
               f"Dans ce cas vous pouvez réserver à nouveau un créneau plus éloigné pour maximiser vos chances d'obtenir une réservation " \
               f"sur <a href='https://www.commissionmedicale.fr'>CommissionMedicale</a> "
    content += f"Nous avons enregistré cette date et elle ne vous sera plus proposée. Par contre si nous trouvons un créneau plus proche " \
               f"de la date que choisi, on vous renverra un email.<br/><br/>"
    content += f"Si vous êtes satisfait de nos services, faites nous part de votre expérience et parlez-en autours de vous :-)<br/>"
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
        write_log(f"Error while sending mail: {e}")
        exit()
    finally:
        server.quit()
        write_log("73kBot sent a mail to 73k05")
