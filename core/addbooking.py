# Add a new booking to the JSON ongoing
import datetime

from model.gouv_endpoint import GouvEndPoint
from utils.converter.json_to_model_converter import to_booking_ongoing
from utils.log import write_server_log


# Add a booking to ongoing booking list
def add_ongoing_booking(booking):
    now = datetime.datetime.now()
    write_server_log(f"[{now.strftime('%d/%m/%y %H:%M')}] Add Booking to ongoing: {booking}")

    # add endpoint to new booking, and save it to db
    add_endpoint_to_booking(booking)
    booking_ongoing = to_booking_ongoing(booking)
    booking_ongoing.save()


# Add endpoint datas to booking and return it
def add_endpoint_to_booking(booking):
    now = datetime.datetime.now()
    region = booking["region"]
    department = GouvEndPoint.objects.raw({"departmentName": region}).first()
    if department is None:
        write_server_log(f"[{now.strftime('%d/%m/%y %H:%M')}] No endpoint found: {region}")
        booking["departmentName"] = ""
        booking["departmentCode"] = ""
        booking["bookUrl"] = ""
        booking["endPointUrl"] = ""
        booking["indexDayZero"] = 0
        return booking

    try:
        write_server_log(f"[{now.strftime('%d/%m/%y %H:%M')}] Endpoint found: {department}")
        booking["departmentName"] = department.departmentName
        booking["departmentCode"] = department.departmentCode
        booking["bookUrl"] = department.bookUrl
        booking["endPointUrl"] = department.endPointUrl
        booking["indexDayZero"] = department.indexDayZero
    except:
        write_server_log(f"[{now.strftime('%H:%M')}] JSON ERROR!")
    return booking
