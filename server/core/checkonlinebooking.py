import datetime
import json
# importing the requests library
import sys
import time

# Time lib to sleep

sys.path.insert(1, '../utils')
from log import writeLog
from dateutils import getdatefromdata
from requestsender import sendGetRequest
from mail import sendMail

# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
bookingOngoingList = {}

# Load dep list
with open('../json/gouvendpoints.json') as json_data:
    urlDepartmentList = json.load(json_data)["gouvUrlList"]

# Load Booking Ongoing List
with open('../../frontend/resources/bookingongoing.json') as json_data:
    bookingList = json.load(json_data)["bookings"]

while 1 == 1:

    nbRequestSent += 1

    # Check all prefs
    for booking in bookingList:
        now = datetime.datetime.now()
        code = booking["department"]
        bookingChooseDate = datetime.datetime.strptime(booking["bookingChooseDate"], "%d/%m/%Y")
        bookedDateStr = booking["bookedCurrentDate"]
        email = booking["email"]

        if bookedDateStr:
            bookedMaxDate = datetime.datetime.strptime(bookedDateStr, "%d/%m/%Y")
        else:
            bookedMaxDate = ""

        department = urlDepartmentList[code - 1]
        endPointUrl = department["endPointUrl"]
        bookUrl = department["bookUrl"]

        writeLog("[" + now.strftime("%H:%M") + "]Booking of: " + email + " code: " + str(
            code) + " request: " + endPointUrl + "0")

        # extracting data in raw text format
        data = sendGetRequest(endPointUrl + "0")
        if data == -1:
            continue

        dateZero = getdatefromdata(data)
        maxDate = max([now, dateZero, bookingChooseDate])

        if dateZero + datetime.timedelta(days=7) >= maxDate and data.find('plage libre') != -1:
            print("Bingo!")
            # TODO: Make booking system
            # params = getParamsFromUser(booking)
            # sendPostRequest(bookUrl, params)
            sendMail("[73b07] /!\\ Free slot for " + email + " /!\\", bookUrl)
            continue
        else:
            bookingTryDate = maxDate
            dayDelta = (maxDate - dateZero).days
            # If not already booked slot for this booking
            # we set it to 1 month max ahead from now to avoid forever tries
            if not bookedMaxDate:
                bookedMaxDate = now + datetime.timedelta(days=60)
            while bookedMaxDate > bookingTryDate:
                data = sendGetRequest(endPointUrl + str(dayDelta))
                if data == -1:
                    break
                elif data.find('plage libre') != -1:
                    print("Bingo!")
                    # TODO: Make booking system
                    sendMail("[73b07] /!\\ Free slot for " + email + " /!\\", bookUrl)
                    break
                bookingTryDate = bookingTryDate + datetime.timedelta(days=7)
                dayDelta += 7

    # Sleeping time in minutes
    sleeptime = 1

    writeLog(f"============ 73kBot will sleep {str(sleeptime)} minutes _o/ {str(nbRequestSent)} ============\r\n")

    time.sleep(sleeptime * 60)
