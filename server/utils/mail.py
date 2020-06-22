import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import project files
import sys
sys.path.insert(1, '../utils')
from log import write_log

# Password
pass_mail = ""
with open('../json/config.json') as json_data:
    pass_mail = json.load(json_data)["creds"]


def createBody(date_free_slot, booking):
    content = f"Bonjour {booking['firstname']},<br/><br/>"
    content += f"Merci d'avoir réservé sur <a href='https://www.commissionmedicale.fr'>CommissionMedicale</a>. Nous avons trouvé un créneau pouvant vous interesser. "
    content += f"Rendez-vous au plus vite sur <a href={booking['bookUrl']}>le site du gouvernement</a>, la date {date_free_slot.strftime('%d/%m/%Y')} est disponible. " \
               f"Si le créneau {date_free_slot.strftime('%d/%m/%Y')} n'est plus disponible, notre outil est déjà en train de chercher une meilleure date pour vous.<br/><br/>" \
               f"Dans le cas où le créneau {date_free_slot.strftime('%d/%m/%Y')} est proche de la date souhaitée, " \
               f"moins d'une semaine par exemple, il sera difficile d'en trouver un plus encore proche. " \
               f"Si ce créneau ne vous convient pas, vous pouvez en réserver un à nouveau, plus éloigné pour maximiser vos chances d'obtenir une réservation " \
               f"sur <a href='https://www.commissionmedicale.fr'>CommissionMedicale</a>. "
    content += f"Nous avons enregistré cette date et elle ne vous sera plus proposée. Par contre, si nous trouvons un créneau plus proche " \
               f"de la date que vous avez choisi, un nouvel email vous sera envoyé.<br/><br/>"
    content += f"Nous souhaitons vous donner plus de chances d'obtenir la réservation en vous proposant une réservation automatique, si cela vous intéresse, vous pouvez répondre" \
               f" à notre <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAZAAIO-KVxUN0FDNDBLWlhQVjNSODJGRkpIUUpGOE9OWC4u'>questionnaire</a><br/><br/>"
    content += f"Bonne conduite<br/>Bob"
    return content


def send_mail(subject, date_free_slot, booking):
    if not pass_mail or pass_mail == "":
        write_log("Sending mail impossible, creds missing, GOTO gouv/server/json/config.json")
        return

    # Server config
    port = 587  # For SSL
    smtp_server = "mail34.lwspanel.com"
    sender_email = "booking@commissionmedicale.fr"  # Enter your address
    receiver_email = booking["email"]
    bcc = "contact@commissionmedicale.fr"
    password = pass_mail

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
        ehlo()
        starttls()
        ehlo()
        login(sender_email, password)
        sendmail(sender_email, toaddrs, text)
    except Exception as e:
        # Print any error messages to stdout
        write_log(f"Error while sending mail: {e}")
    finally:
        quit()
        write_log("73kBot sent a mail to 73k05")
