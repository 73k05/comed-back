import datetime

# import project files
from model.department_availability import DepartmentAvailability
from model.gouv_endpoint import GouvEndPoint
from utils.bookingutils import get_open_slot
from utils.log import write_log


class UpdateDepartmentAvailabilities:
    cancelJob = False

    @staticmethod
    def save_department_availability(department_code, department_name, booking, department_book_url):
        date_free_slot = "" if not booking["date"] else booking["date"].strftime("%Y-%m-%d")
        department_availability = DepartmentAvailability()
        department_availability.departmentCode = department_code
        department_availability.departmentName = department_name
        department_availability.bookingOpen = booking["is_open"]
        department_availability.bookingFirstOpenSlotDate = date_free_slot
        department_availability.departmentBookUrl = department_book_url
        department_availability.save()

    def update_department_availabilities_job(self):
        # Count number of request sent
        nb_request_sent = 0
        url_department_list = {}
        # Set it to zero to update all departments
        department_start_index = 0
        # Set it to high value to update all departments
        department_stop_index = 150
        max_day_to_look_forward = 120

        # Check all prefs
        for gouv_endpoint in GouvEndPoint.objects.all():
            if self.cancelJob:
                return
            nb_request_sent += 1

            department_code = gouv_endpoint.departmentCode
            department_name = gouv_endpoint.departmentName
            department_book_url = gouv_endpoint.bookUrl

            # Bypass this department if needed for efficient testing sometimes
            if gouv_endpoint.bypass or nb_request_sent < department_start_index or\
                    nb_request_sent > department_stop_index:
                write_log("Skip dep!")
                self.save_department_availability(department_code, department_name, {"is_open": False, "date": ""},
                                                  department_book_url)
                continue

            booking = get_open_slot(gouv_endpoint, max_day_to_look_forward, datetime.datetime.now())
            write_log(f"Department availability: {booking}")
            self.save_department_availability(department_code, department_name, booking, department_book_url)

        write_log(f"============ 73kBot successfully updated department availabilities _o/"
                  f" {str(nb_request_sent)} ============")
