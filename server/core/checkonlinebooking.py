import copy
import datetime
import json
# importing the requests library
import sys

sys.path.insert(1, '../utils')
import time
from bookingutils import get_open_slot
from mail import send_mail
# Time lib to sleep
from log import write_log

from jsonutils import write_ongoing_booking, write_bk_booking

# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
bookingOngoingList = {}
maxDayToLookForward = 120

while 1 == 1:

    # Load Booking Ongoing List
    with open('../../frontend/resources/json/bookingongoing.json') as json_data:
        bookingList = json.load(json_data)["bookings"]
        bookingListCopy = copy.copy(bookingList)

    with open('../json/bk_booking.json') as json_data:
        bk_bookingList = json.load(json_data)["bookings"]

    nbRequestSent += 1

    # Check all prefs
    for booking in bookingList:
        now = datetime.datetime.now()
        write_log("[" + now.strftime("%H:%M") + "] Booking...")

        code = booking["departmentCode"]
        booking_choose_date = datetime.datetime.strptime(booking["bookingChooseDate"], "%d/%m/%Y")
        booked_date = datetime.datetime.now() + datetime.timedelta(days=maxDayToLookForward) if not booking[
            "bookedCurrentDate"] else datetime.datetime.strptime(booking["bookedCurrentDate"], "%d/%m/%Y")
        email = booking["email"]
        book_url = booking["bookUrl"]

        # Purge file
        if booked_date < now or booking_choose_date < now:
            bookingListCopy.remove(booking)
            bk_bookingList.append(booking)
            continue

        booking_slot = get_open_slot(booking, maxDayToLookForward, booking_choose_date)
        write_log(f"Department availability: {booking_slot}")
        date_free_slot = -1 if not booking_slot["date"] else booking_slot["date"]
        minimum_book_date = max(datetime.datetime.now(), booking_choose_date)
        if booking_slot[
            "is_open"] and date_free_slot != -1 and booked_date > date_free_slot > minimum_book_date:
            write_log(f"/!\\Slot found, sending email/!\\")
            send_mail("[CoMed] Réservation trouvée", date_free_slot, booking)
            booking["bookedCurrentDate"] = date_free_slot.strftime("%d/%m/%Y")

    write_ongoing_booking(bookingListCopy)
    write_bk_booking(bk_bookingList)

    # Sleeping time in minutes
    sleeptime = 60

    write_log(f"============ 73kBot will sleep {str(sleeptime)} minutes _o/ {str(nbRequestSent)} ============")

    time.sleep(sleeptime * 60)
