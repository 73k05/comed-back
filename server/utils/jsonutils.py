import json


# Write in json file
def write_department_availability(departments):
    with open('../../frontend/resources/json/departmentavailabilities.json', "w+") as json_file:
        json_data = {"departments": departments}
        json.dump(json_data, json_file)


def add_department_to_list(department_code, department_name, date, department_availability_list):
    date_free_slot = "" if not date else date.strftime("%Y-%m-%d")
    department_availability_list.append({
        "departmentCode": department_code,
        "departmentName": department_name,
        "bookingFirstOpenSlotDate": date_free_slot
    })
