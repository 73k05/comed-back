import copy
import datetime
import json
# importing the requests library
import sys
from server.utils.bookingutils import get_open_slot
from server.utils.mail import send_mail
# Time lib to sleep
from server.utils.log import write_log
from server.utils.jsonutils import write_ongoing_booking, write_bk_booking


class CheckOnlineBooking:
    cancelJob = False

    def check_online_booking_job(self):
        # Count number of request sent
        nb_request_sent = 0
        max_day_to_look_forward = 120

        # Load Booking Ongoing List
        with open('../json/booking_ongoing.json') as json_data:
            booking_list = json.load(json_data)["bookings"]
            booking_list_copy = copy.copy(booking_list)

        with open('../json/bk_booking.json') as json_data:
            bk_booking_list = json.load(json_data)["bookings"]

        nb_request_sent += 1

        # Check all prefs
        for booking in booking_list:
            # to handle server stop without waiting the end of job
            if self.cancelJob:
                return
            now = datetime.datetime.now()
            write_log("[" + now.strftime("%H:%M") + "] Booking...")

            code = booking["departmentCode"]
            booking_choose_date = datetime.datetime.strptime(booking["bookingChooseDate"], "%d/%m/%Y")
            booked_date = datetime.datetime.now() + datetime.timedelta(days=max_day_to_look_forward) if not booking[
                "bookedCurrentDate"] else datetime.datetime.strptime(booking["bookedCurrentDate"], "%d/%m/%Y")
            email = booking["email"]
            book_url = booking["bookUrl"]

            # Purge file
            if booked_date < now or booking_choose_date < now:
                booking_list_copy.remove(booking)
                bk_booking_list.append(booking)
                continue

            booking_slot = get_open_slot(booking, max_day_to_look_forward, booking_choose_date)
            write_log(f"Department availability: {booking_slot}")
            date_free_slot = -1 if not booking_slot["date"] else booking_slot["date"]
            minimum_book_date = max(datetime.datetime.now(), booking_choose_date)
            if booking_slot[
                "is_open"] and date_free_slot != -1 and booked_date > date_free_slot >= minimum_book_date:
                write_log(f"/!\\Slot found, sending email/!\\")
                send_mail("[CoMed] Créneau disponible", date_free_slot, booking)
                booking["bookedCurrentDate"] = date_free_slot.strftime("%d/%m/%Y")

        write_ongoing_booking(booking_list_copy)
        write_bk_booking(bk_booking_list)

        write_log(f"============ 73kBot successfully updated online booking _o/ {str(nb_request_sent)} ============")
