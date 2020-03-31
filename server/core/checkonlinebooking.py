import datetime
from datetime import time
import json
# importing the requests library
import sys

# Time lib to sleep

sys.path.insert(1, '../utils')
from log import writeLog
from dateutils import getdatefromdata
from requestsender import sendGetRequest

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
        urlEndPoint = urlDepartmentList[code - 1]["url"]

        writeLog("[" + now.strftime("%H:%M") + "]Booking of: " + booking[
            "email"] + " code: " + str(code) + " request: " + urlEndPoint + "0")

        # extracting data in raw text format
        data = sendGetRequest(urlEndPoint + "0")
        if(data == -1):
            continue

        dateZero = getdatefromdata(data)
        maxDate = max([now, dateZero, bookingChooseDate])

        if dateZero == maxDate and data.find('plage libre') != -1:
            print("Bingo!")
        else:
            dayDelta = (maxDate - dateZero).days

    # Sleeping time in minutes
    sleeptime = 1

    writeLog("============ 73kBot will sleep " + str(sleeptime) + " minutes _o/ " + str(
        nbRequestSent) + " ============" + "\r\n")

    time.sleep(sleeptime * 60)
