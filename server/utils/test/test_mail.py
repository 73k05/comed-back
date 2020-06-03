import datetime
import sys

sys.path.insert(1, '../utils')
from mail import send_mail

now = datetime.datetime.now()
send_mail("73K05 Test mail ok!", now, {'email': 'contact@commissionmedicale.fr', 'bookUrl': 'TEST', 'firstname':'TEST'})
