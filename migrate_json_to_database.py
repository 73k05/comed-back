import json

from pymodm.connection import connect
from model.booking_ongoing import BookingOngoing
from model.department_availability import DepartmentAvailability
from model.gouv_endpoint import GouvEndPoint
from utils.converter.json_to_model_converter import to_booking_ongoing, to_gouv_endpoint, to_department_availability

from config.configuration_manager import ConfigurationManager

config = ConfigurationManager()
DB_URL = config.active_configuration['DATABASE_URL']
connect(DB_URL)

with open('json/gouvendpoints.json') as json_data:
    url_department_list = json.load(json_data)["gouvUrlList"]

# Creates gouv endpoint in db
gouv_endpoints = []
for department_json in url_department_list:
    gouv_endpoints.append(to_gouv_endpoint(department_json))
GouvEndPoint.objects.bulk_create(gouv_endpoints)

with open('json/booking_ongoing.json') as json_data:
    bookings = json.load(json_data)["bookings"]

# Creates bookings in db
bookings_ongoing = []
for booking_json in bookings:
    bookings_ongoing.append(to_booking_ongoing(booking_json))
BookingOngoing.objects.bulk_create(bookings_ongoing)

with open('json/department_availabilities.json') as json_data:
    department_availabilities_json = json.load(json_data)["departments"]

# Creates department availabilities in db
department_availabilities = []
for department_avail_json in department_availabilities_json:
    department_availabilities.append(to_department_availability(department_avail_json))
DepartmentAvailability.objects.bulk_create(department_availabilities)
