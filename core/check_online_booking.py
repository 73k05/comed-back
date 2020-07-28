import datetime

# import project files
from model.booking_ongoing import BookingOngoing
from utils.bookingutils import get_open_slot
# Time lib to sleep
from utils.log import write_log
from utils.mail import send_mail


class CheckOnlineBooking:
    cancelJob = False

    def check_online_booking_job(self):
        # Count number of request sent
        nb_request_sent = 0
        max_day_to_look_forward = 120
        nb_request_sent += 1

        # Check all prefs
        for booking in BookingOngoing.objects.raw({"archived": False}):
            # to handle server stop without waiting the end of job
            if self.cancelJob:
                return
            now = datetime.datetime.now()
            write_log("[" + now.strftime("%d/%m/%y %H:%M") + "] Booking...")

            booking_choose_date = booking.bookingChooseDate
            booked_date = datetime.datetime.now() + datetime.timedelta(days=max_day_to_look_forward) if not booking\
                .bookedCurrentDate else booking.bookedCurrentDate

            # Tag as archived
            if booked_date < now or booking_choose_date < now:
                booking.archived = True
                booking.save()
                continue

            booking_slot = get_open_slot(booking, max_day_to_look_forward, booking_choose_date)
            write_log(f"Department availability: {booking_slot}")
            date_free_slot = -1 if not booking_slot["date"] else booking_slot["date"]
            minimum_book_date = max(datetime.datetime.now(), booking_choose_date)
            if booking_slot["is_open"] and date_free_slot != -1 and booked_date > date_free_slot >= minimum_book_date:
                write_log(f"/!\\Slot found, sending email/!\\")
                if send_mail("[CoMed] Créneau disponible", date_free_slot, booking):
                    booking.bookedCurrentDate = date_free_slot
                    booking.save()

        write_log(f"============ 73kBot successfully updated online booking _o/ {str(nb_request_sent)} ============")
