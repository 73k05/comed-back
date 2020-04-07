import datetime
import json
import sys
import time

from dateutils import getdatefromdata
from dateutils import update_index_day_zero_to_today
from jsonutils import add_department_to_list
from jsonutils import write_department_availability
from log import writeLog
from requestsender import sendGetRequest

sys.path.insert(1, '../utils')

# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
departmentStartIndex = 0
indexDep = 0
maxDayToLookForward = 60

while 1 == 1:

    # Load dep list
    with open('../json/gouvendpoints.json') as json_data:
        urlDepartmentList = json.load(json_data)["gouvUrlList"]

    departmentAvailabilityList = []

    nbRequestSent += 1

    # Check all prefs
    for departmentEndpoint in urlDepartmentList:
        departmentCode = departmentEndpoint["departmentCode"]
        departmentName = departmentEndpoint["departmentName"]
        endPointUrl = departmentEndpoint["endPointUrl"]
        departmentBookUrl = departmentEndpoint["bookUrl"]
        indexDayZero = departmentEndpoint["indexDayZero"]

        now = datetime.datetime.now()
        writeLog("[" + now.strftime("%H:%M") + "] Department " + str(departmentName) + " availability update...")

        indexDep += 1
        if departmentEndpoint["bypass"] == 1 or indexDep < departmentStartIndex:
            writeLog(f"Skip dep!")
            continue

        if not endPointUrl:
            continue

        isSlotAvailableFound = False

        writeLog("Booking of: " + str(departmentCode) + " request: " + endPointUrl + str(indexDayZero))

        # extracting data in raw text format
        data = sendGetRequest(endPointUrl + str(indexDayZero))
        if data == -1:
            continue

        dateZero = getdatefromdata(data)

        if dateZero >= now and data.find('plage libre') != -1:
            writeLog("/!\\ Free slot Bingo /!\\")
            isSlotAvailableFound = True
            add_department_to_list(departmentCode, departmentName, dateZero, departmentBookUrl,
                                   departmentAvailabilityList)
            continue
        else:
            dayDelta = update_index_day_zero_to_today(indexDayZero, dateZero, now)
            # If not already booked slot for this booking
            # we set it to 1 month max ahead from now to avoid forever tries
            # if not bookedMaxDate:
            bookingTryDate = max([now, dateZero])
            bookedMaxDate = bookingTryDate + datetime.timedelta(days=maxDayToLookForward)
            while bookedMaxDate > bookingTryDate:
                data = sendGetRequest(endPointUrl + str(dayDelta))
                if data == -1:
                    break
                elif data.find('plage libre') != -1:
                    writeLog("/!\\ Free slot Bingo /!\\")
                    isSlotAvailableFound = True
                    add_department_to_list(departmentCode, departmentName, bookingTryDate, departmentBookUrl,
                                           departmentAvailabilityList)
                    break
                bookingTryDate = bookingTryDate + datetime.timedelta(days=7)
                dayDelta += 7
        if not isSlotAvailableFound:
            add_department_to_list(departmentCode, departmentName, "", departmentBookUrl, departmentAvailabilityList)
        # TODO: Check front for availability
        # else:
            # indexFooter = data.find('<footer>')
            # found = data.find('ultérieurement', 0, (indexFooter)) != -1

    write_department_availability(departmentAvailabilityList)

    # Sleeping time in minutes
    sleeptime = 60

    writeLog(f"============ 73kBot will sleep {str(sleeptime)} minutes _o/ {str(nbRequestSent)} ============\r\n")

    time.sleep(sleeptime * 60)
