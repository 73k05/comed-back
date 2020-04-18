import json
import sys
import time
import datetime

from bookingutils import get_open_slot
from jsonutils import add_department_to_list
from jsonutils import write_department_availability
from log import writeLog

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
    for department in urlDepartmentList:
        nbRequestSent += 1

        departmentCode = department["departmentCode"]
        departmentName = department["departmentName"]
        departmentBookUrl = department["bookUrl"]

        # Bypass this department if needed for efficient testing sometimes
        if department["bypass"] or nbRequestSent < departmentStartIndex or nbRequestSent > departmentStopIndex:
            writeLog("Skip dep!")
            add_department_to_list(departmentCode, departmentName, {"is_open": False, "date": ""}, departmentBookUrl,
                                   departmentAvailabilityList)
            continue

        booking = get_open_slot(department, maxDayToLookForward, datetime.datetime.now())
        writeLog(f"Department availability: {booking}")
        add_department_to_list(departmentCode, departmentName, booking, departmentBookUrl,
                               departmentAvailabilityList)

    write_department_availability(departmentAvailabilityList)

    # Sleeping time in minutes
    sleep_time = 60

    writeLog(f"============ 73kBot will sleep {str(sleep_time)} minutes _o/ {str(nbRequestSent)} ============\r\n")

    time.sleep(sleep_time * 60)
