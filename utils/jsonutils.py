import json
from shutil import copyfile


def write_department_availability(departments):
    dep_availability_json = 'json/department_availabilities.json'
    copyfile(dep_availability_json, 'json/department_availabilities_bk.json')
    with open(dep_availability_json, "w+") as json_file:
        json_data = {"departments": departments}
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)


# Write backup in json file
def write_bk_booking(bookings):
    bookings_json = 'json/booking_ongoing_bk.json'
    write_booking(bookings, bookings_json)


# Write ongoing in json file
def write_ongoing_booking(bookings):
    bookings_json = 'json/booking_ongoing.json'
    write_booking(bookings, bookings_json)


# Write in json file
def write_booking(bookings, bookings_json):
    with open(bookings_json, "w", encoding='utf-8') as json_file:
        json_data = {"bookings": bookings}
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)


def add_department_to_list(department_code, department_name, booking, department_book_url,
                           department_availability_list):
    date_free_slot = "" if not booking["date"] else booking["date"].strftime("%Y-%m-%d")
    department_availability_list.append({
        "departmentCode": department_code,
        "departmentName": department_name,
        "bookingOpen": booking["is_open"],
        "bookingFirstOpenSlotDate": date_free_slot,
        "departmentBookUrl": department_book_url
    })
