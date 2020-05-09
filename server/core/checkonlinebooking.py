import datetime
import json
# importing the requests library
import sys
sys.path.insert(1, '../utils')
import time
from bookingutils import get_open_slot
from mail import sendMail
# Time lib to sleep
from log import writeLog


# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
bookingOngoingList = {}
maxDayToLookForward = 60

while 1 == 1:

    # Load Booking Ongoing List
    with open('../../frontend/resources/json/bookingongoing.json') as json_data:
        bookingList = json.load(json_data)["bookings"]

    nbRequestSent += 1

    # Check all prefs
    for booking in bookingList:
        now = datetime.datetime.now()
        writeLog("[" + now.strftime("%H:%M") + "] Booking...")

        code = booking["departmentCode"]
        booking_choose_date = datetime.datetime.strptime(booking["bookingChooseDate"], "%d/%m/%Y")
        booked_date = datetime.datetime.now() if not booking["bookedCurrentDate"] else datetime.datetime.strptime(booking["bookedCurrentDate"], "%d/%m/%Y")
        email = booking["email"]
        book_url = booking["bookUrl"]

        booking_slot = get_open_slot(booking, maxDayToLookForward, booking_choose_date)
        writeLog(f"Department availability: {booking_slot}")
        date_free_slot = -1 if not booking_slot["date"] else booking_slot["date"]
        if booking_slot["is_open"] and date_free_slot != -1 and date_free_slot < booked_date:
            sendMail("[73b07] /!\\ Free slot for " + email + " /!\\", book_url)

    # Sleeping time in minutes
    sleeptime = 60

    writeLog(f"============ 73kBot will sleep {str(sleeptime)} minutes _o/ {str(nbRequestSent)} ============")

    time.sleep(sleeptime * 60)
