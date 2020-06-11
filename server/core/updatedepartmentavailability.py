import datetime
import json
from server.utils.bookingutils import get_open_slot
from server.utils.jsonutils import add_department_to_list
from server.utils.jsonutils import write_department_availability
from server.utils.log import write_log

# Count number of request sent
nbRequestSent = 0
urlDepartmentList = {}
# Set it to zero to update all departments
departmentStartIndex = 0
# Set it to high value to update all departments
departmentStopIndex = 150
maxDayToLookForward = 120

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
        write_log("Skip dep!")
        add_department_to_list(departmentCode, departmentName, {"is_open": False, "date": ""}, departmentBookUrl,
                               departmentAvailabilityList)
        continue

    booking = get_open_slot(department, maxDayToLookForward, datetime.datetime.now())
    write_log(f"Department availability: {booking}")
    add_department_to_list(departmentCode, departmentName, booking, departmentBookUrl,
                           departmentAvailabilityList)

write_department_availability(departmentAvailabilityList)

write_log(f"============ 73kBot will sleep forever _o/ {str(nbRequestSent)} ============")
