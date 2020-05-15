import json
from shutil import copyfile


# Write in json file
from log import write_server_log


def write_department_availability(departments):
    dep_availability_json = '../../frontend/resources/json/departmentavailabilities.json'
    copyfile(dep_availability_json, '../../frontend/resources/json/departmentavailabilities_bk.json')
    with open(dep_availability_json, "w+") as json_file:
        json_data = {"departments": departments}
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)


# Write in json file
def write_ongoing_booking(bookings):
    write_server_log(f"write_ongoing_booking...")
    bookings_json = '../../frontend/resources/json/bookingongoing.json'
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
