# Add a new booking to the JSON ongoing
import json

# Load Booking Ongoing List
from jsonutils import write_ongoing_booking


def add_ongoing_booking(booking):
    with open('../../frontend/resources/json/bookingongoing.json') as json_data:
        bookingList = json.load(json_data)["bookings"]

        bookingList.append(add_endpoint_to_booking(booking))

        write_ongoing_booking(bookingList)


def add_endpoint_to_booking(booking):
    with open('../json/gouvendpoints.json') as json_data:
        urlDepartmentList = json.load(json_data)["gouvUrlList"]
        for department in urlDepartmentList:
            departmentName = department["departmentName"]
            if departmentName == booking["region"]:
                booking["departmentName"] = department["departmentName"]
                booking["departmentCode"] = department["departmentCode"]
                booking["bookUrl"] = department["bookUrl"]
                booking["endPointUrl"] = department["endPointUrl"]
                booking["indexDayZero"] = department["indexDayZero"]
                break
    return booking