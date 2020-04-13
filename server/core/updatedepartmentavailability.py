import datetime
import json
import sys
import time

from dateutils import get_date_from_data
from dateutils import update_index_day_zero_to_today
from jsonutils import add_department_to_list
from jsonutils import write_department_availability
from log import writeLog
from requestsender import send_get_request
from requestsender import send_post_request

sys.path.insert(1, '../utils')

# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
# Set it to zero to update all departments
departmentStartIndex = 0
# Set it to high value to update all departments
departmentStopIndex = 150
maxDayToLookForward = 60

while 1 == 1:

    # Load dep list
    with open('../json/gouvendpoints.json') as json_data:
        urlDepartmentList = json.load(json_data)["gouvUrlList"]

    departmentAvailabilityList = []

    # Check all prefs
    for departmentInfos in urlDepartmentList:
        nbRequestSent += 1

        departmentCode = departmentInfos["departmentCode"]
        departmentName = departmentInfos["departmentName"]
        endPointUrl = departmentInfos["endPointUrl"]
        departmentBookUrl = departmentInfos["bookUrl"]
        dayZero = departmentInfos["indexDayZero"]

        now = datetime.datetime.now()
        writeLog("[" + now.strftime("%H:%M") + "] Department " + str(departmentName) + " availability update...")

        depCodeIndex = nbRequestSent
        if isinstance(departmentCode, int):
            depCodeIndex = int(departmentCode)
        if departmentInfos["bypass"] or depCodeIndex < departmentStartIndex or depCodeIndex > departmentStopIndex:
            writeLog("Skip dep!")
            add_department_to_list(departmentCode, departmentName, False, "", departmentBookUrl,
                                   departmentAvailabilityList)
            continue

        if not endPointUrl:
            writeLog("EndPoint null!")
            continue

        isSlotAvailableFound = False

        # extracting data in raw text format
        data = send_get_request(endPointUrl + str(dayZero))
        # TODO set dep in json anyways
        if data == -1:
            continue

        dateZero = get_date_from_data(data)
        dayDelta = update_index_day_zero_to_today(dayZero, dateZero, now)
        # Add days to try_date to be the same as day_delta date
        bookingTryDate = max([now, dateZero + datetime.timedelta(days=dayDelta - dayZero)])

        # If not already booked slot for this booking
        # we set it to 1 month max ahead from now to avoid forever tries
        # if not bookedMaxDate:
        bookedMaxDate = bookingTryDate + datetime.timedelta(days=maxDayToLookForward)
        while bookedMaxDate > bookingTryDate:
            data = send_get_request(endPointUrl + str(dayDelta))
            if data == -1:
                break
            elif data.find('plage libre') != -1:
                isSlotAvailableFound = True
                break
            bookingTryDate = bookingTryDate + datetime.timedelta(days=7)
            dayDelta += 7
        # Check front for booking opening
        if isSlotAvailableFound:
            data = send_post_request(departmentBookUrl,
                                     {"condition": "on", "nextButton": 'Effectuer une demande de rendez-vous'})
            if data != -1:
                indexFooter = data.find('<footer>')
                closed_sentence = "Attention : Cette page n'est pas disponible pour le moment !"
                closed = data.find('ultérieurement', 0, indexFooter) != -1 or data.find(closed_sentence, 0,
                                                                                        indexFooter) != -1
            else:
                closed = True
            if closed:
                isSlotAvailableFound = False
        else:
            bookingTryDate = ""

        add_department_to_list(departmentCode, departmentName, isSlotAvailableFound, bookingTryDate, departmentBookUrl,
                               departmentAvailabilityList)

    write_department_availability(departmentAvailabilityList)

    # Sleeping time in minutes
    sleep_time = 60

    writeLog(f"============ 73kBot will sleep {str(sleep_time)} minutes _o/ {str(nbRequestSent)} ============\r\n")

    time.sleep(sleep_time * 60)
