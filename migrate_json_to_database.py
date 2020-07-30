import json

from pymodm.connection import connect
from utils.converter.json_to_model_converter import to_booking_ongoing, to_gouv_endpoint, to_department_availability

from config.configuration_manager import ConfigurationManager

config = ConfigurationManager()
DB_URL = config.active_configuration['DATABASE_URL']
connect(DB_URL)

with open('json/gouvendpoints.json') as json_data:
    url_department_list = json.load(json_data)["gouvUrlList"]

# Creates gouv endpoint in db
for department_json in url_department_list:
    gouv_endpoint = to_gouv_endpoint(department_json)
    gouv_endpoint.save()

with open('json/booking_ongoing.json') as json_data:
    bookings = json.load(json_data)["bookings"]

# Creates bookings in db
for booking_json in bookings:
    booking_ongoing = to_booking_ongoing(booking_json)
    booking_ongoing.save()

with open('json/department_availabilities.json') as json_data:
    department_availabilities = json.load(json_data)["departments"]

# Creates department availabilities in db
for department_avail_json in department_availabilities:
    department_availability = to_department_availability(department_avail_json)
    department_availability.save()
