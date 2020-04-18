import json
from shutil import copyfile


# Write in json file
def write_department_availability(departments):
    dep_availability_json = '../../frontend/resources/json/departmentavailabilities.json'
    copyfile(dep_availability_json, '../../frontend/resources/json/departmentavailabilities_bk.json')
    with open(dep_availability_json, "w+") as json_file:
        json_data = {"departments": departments}
        json.dump(json_data, json_file)


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
