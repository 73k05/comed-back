import datetime

from utils.mail import send_mail

now = datetime.datetime.now()
send_mail("73K05 Test mail ok!", now, {'email': 'contact@commissionmedicale.fr', 'bookUrl': 'TEST', 'firstname':'TEST'})
