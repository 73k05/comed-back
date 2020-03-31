import datetime
import json
# importing the requests library
import sys
# Time lib to sleep
import time

import requests
from requests.exceptions import HTTPError

sys.path.insert(1, '../utils')
from log import writeLog
from dateutils import getmonthfromfrench
from dateutils import getdatefromdata

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

# fake header to bypass security
headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

while 1 == 1:

    nbRequestSent += 1

    # Check all prefs
    for booking in bookingList:
        now = datetime.datetime.now()
        code = booking["department"]
        urlEndPoint = urlDepartmentList[code - 1]["url"]
        print(urlDepartmentList[code - 1])
        writeLog("[" + now.strftime("%H:%M") + "]Booking of: " + booking[
            "email"] + " code: " + str(code) + " request: " + urlEndPoint)
        # Send request to gouv
        # sending get request and saving the response as response object
        try:
            response = requests.get(urlEndPoint, headers=headers)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            writeLog(f"\r\nRequest HTTP error occurred: {http_err}\r\n")  # Python 3.6
            break
        except Exception as err:
            writeLog(f"\r\nRequest Other error occurred: {err}\r\n")  # Python 3.6
            break
        else:
            # extracting data in raw text format
            # data = response.content
            data = response.text

            dateZero = getdatefromdata(data)
            print(dateZero.strftime("%d/%m/%y"))

            found = data.find('plage libre', 0) != -1
            writeLog(f"Found: {found} \r\n")
            # Send email when slot found
            if found:
                writeLog(": [OPEN]\r\n")
                print("Bingo!")
            # Send email when slot found
            else:
                writeLog(": [CLOSED]\r\n")
                print("Close -_-")

    # Sleeping time in minutes
    sleeptime = 1

    writeLog("============ 73kBot will sleep " + str(sleeptime) + " minutes _o/ " + str(
        nbRequestSent) + " ============" + "\r\n")

    time.sleep(sleeptime * 60)
