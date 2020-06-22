import datetime
import json
from utils.bookingutils import get_open_slot
from utils.jsonutils import add_department_to_list
from utils.jsonutils import write_department_availability
from utils.log import write_log


class UpdateDepartmentAvailabilities:
    cancelJob = False

    def update_department_availabilities_job(self):
        # Count number of request sent
        nbRequestSent = 0
        url_department_list = {}
        # Set it to zero to update all departments
        department_start_index = 0
        # Set it to high value to update all departments
        department_stop_index = 150
        max_day_to_look_forward = 120

        # Load dep list
        with open('../json/gouvendpoints.json') as json_data:
            url_department_list = json.load(json_data)["gouvUrlList"]

        department_availability_list = []

        # Check all prefs
        for department in url_department_list:
            if self.cancelJob:
                return
            nbRequestSent += 1

            department_code = department["departmentCode"]
            department_name = department["departmentName"]
            department_book_url = department["bookUrl"]

            # Bypass this department if needed for efficient testing sometimes
            if department["bypass"] or nbRequestSent < department_start_index or nbRequestSent > department_stop_index:
                write_log("Skip dep!")
                add_department_to_list(department_code, department_name, {"is_open": False, "date": ""}, department_book_url,
                                       department_availability_list)
                continue

            booking = get_open_slot(department, max_day_to_look_forward, datetime.datetime.now())
            write_log(f"Department availability: {booking}")
            add_department_to_list(department_code, department_name, booking, department_book_url,
                                   department_availability_list)

        write_department_availability(department_availability_list)

        write_log(f"============ 73kBot successfully updated department availabilities _o/ {str(nbRequestSent)} ============")
