from model.booking_ongoing import BookingOngoing
from model.department_availability import DepartmentAvailability
from model.gouv_endpoint import GouvEndPoint
from utils.dateutils import string_to_date


def to_booking_ongoing(json_item):
    booking = BookingOngoing()
    booking.email = json_item["email"]
    booking.firstName = json_item["firstname"]
    booking.lastName = json_item["lastname"]
    booking.phone = json_item["phone"]
    booking.number = json_item["number"]
    booking.birthDate = string_to_date(json_item["birthdate"])
    booking.birthName = json_item["birthname"]
    booking.region = json_item["region"]
    booking.typeVisit = json_item["typevisit"]
    booking.bookingChooseDate = string_to_date(json_item["bookingChooseDate"])
    # avoid resetting booked current date if user subscribe twice
    if json_item["bookedCurrentDate"]:
        booking.bookedCurrentDate = string_to_date(json_item["bookedCurrentDate"])
    booking.addressStreet = json_item["addressStreet"]
    booking.addressZip = json_item["addressZip"]
    booking.addressCity = json_item["addressCity"]
    booking.departmentName = json_item["departmentName"]
    booking.departmentCode = json_item["departmentCode"]
    booking.bookUrl = json_item["bookUrl"]
    booking.endPointUrl = json_item["endPointUrl"]
    booking.indexDayZero = json_item["indexDayZero"]
    booking.purged = False
    return booking


def to_gouv_endpoint(json_item):
    gouv_endpoint = GouvEndPoint()
    gouv_endpoint.departmentCode = json_item["departmentCode"]
    gouv_endpoint.departmentName = json_item["departmentName"]
    gouv_endpoint.bypass = json_item["bypass"]
    gouv_endpoint.endPointUrl = json_item["endPointUrl"]
    gouv_endpoint.indexDayZero = json_item["indexDayZero"]
    gouv_endpoint.bookUrl = json_item["bookUrl"]
    return gouv_endpoint


def to_department_availability(json_item):
    department_availability = DepartmentAvailability()
    department_availability.departmentCode = json_item["departmentCode"]
    department_availability.departmentName = json_item["departmentName"]
    department_availability.bookingOpen = json_item["bookingOpen"]
    department_availability.bookingFirstOpenSlotDate = json_item["bookingFirstOpenSlotDate"]
    department_availability.departmentBookUrl = json_item["departmentBookUrl"]
    return department_availability
