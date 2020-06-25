# Add a new booking to the JSON ongoing
import datetime
import json
#import project files
from utils.log import write_server_log
from utils.jsonutils import write_ongoing_booking


# Add a booking to ongoing booking list
def add_ongoing_booking(booking):
    now = datetime.datetime.now()
    write_server_log(f"[{now.strftime('%d/%m/%y %H:%M')}] Add Booking to ongoing: {booking}")
    with open('../json/booking_ongoing.json', "r", encoding='utf-8') as json_data:
        bookingList = json.load(json_data)["bookings"]

    bookingList.append(add_endpoint_to_booking(booking))

    write_ongoing_booking(bookingList)


# Add endpoint datas to booking and return it
def add_endpoint_to_booking(booking):
    now = datetime.datetime.now()
    with open('../json/gouvendpoints.json', "r", encoding='utf-8') as json_data:
        urlDepartmentList = json.load(json_data)["gouvUrlList"]
    for department in urlDepartmentList:
        try:
            departmentName = department["departmentName"]
            if departmentName == booking["region"]:
                write_server_log(f"[{now.strftime('%d/%m/%y %H:%M')}] Endpoint found: {department}")
                booking["departmentName"] = department["departmentName"]
                booking["departmentCode"] = department["departmentCode"]
                booking["bookUrl"] = department["bookUrl"]
                booking["endPointUrl"] = department["endPointUrl"]
                booking["indexDayZero"] = department["indexDayZero"]
                break
        except:
            write_server_log(f"[{now.strftime('%H:%M')}] JSON ERROR!")
            break
    return booking
