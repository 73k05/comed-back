import datetime

from dateutils import get_date_from_data
from dateutils import update_index_day_zero_to_today
from log import writeLog
from requestsender import send_get_request
from requestsender import send_post_request

params = {
    "firstname": "Jack",
    "lastname": "Bolet",
    "email": "qdfgfaezrr@yopmail.com",
    "emailcheck": "qdfgfaezrr@yopmail.com",
    "eZBookingAdditionalField_value_877": "01/01/1991",
    "eZBookingAdditionalField_value_878": "Bolet",
    "eZBookingAdditionalField_value_879": "3 rue Pierre",
    "eZBookingAdditionalField_value_881": "07000",
    "eZBookingAdditionalField_value_882": "Privas"
}


def get_params_from_user(userJson):
    params = {
        "firstname": userJson["firstname"],
        "lastname": userJson["lastname"],
        "email": userJson["email"],
        "emailcheck": userJson["emailcheck"],
        "eZBookingAdditionalField_value_877": userJson["birthDate"],
        "eZBookingAdditionalField_value_878": userJson["lastname"],
        "eZBookingAdditionalField_value_879": userJson["lastname"],
        "eZBookingAdditionalField_value_879": "3 rue Pierre",
        "eZBookingAdditionalField_value_881": "07000",
        "eZBookingAdditionalField_value_882": "Privas"}
    return params


def get_open_slot(department, max_day_to_look_forward, date_wanted):
    department_name = department["departmentName"]
    end_point_url = department["endPointUrl"]
    departmentBookUrl = department["bookUrl"]
    day_zero = department["indexDayZero"]

    writeLog("[" + date_wanted.strftime("%H:%M") + "] Department " + str(department_name) + " availability update...")

    if not end_point_url:
        writeLog("EndPoint null!")
        return {"is_open": False, "date": ""}

    is_slot_available_found = False

    # extracting data in raw text format
    data = send_get_request(end_point_url + str(day_zero))
    if data == -1:
        return {"is_open": False, "date": ""}

    dateZero = get_date_from_data(data)
    dayDelta = update_index_day_zero_to_today(day_zero, dateZero, date_wanted)
    # Add days to try_date to be the same as day_delta date
    bookingTryDate = max([date_wanted, dateZero + datetime.timedelta(days=dayDelta - day_zero)])

    # If not already booked slot for this booking
    # we set it to 1 month max ahead from now to avoid forever tries
    # if not bookedMaxDate:
    bookedMaxDate = bookingTryDate + datetime.timedelta(days=max_day_to_look_forward)
    while bookedMaxDate > bookingTryDate:
        data = send_get_request(end_point_url + str(dayDelta))
        if data == -1:
            break
        elif data.find('plage libre') != -1:
            is_slot_available_found = True
            break
        bookingTryDate = bookingTryDate + datetime.timedelta(days=7)
        dayDelta += 7
    # Check front for booking opening
    if is_slot_available_found:
        data = send_post_request(departmentBookUrl,
                                 {"condition": "on", "nextButton": 'Effectuer une demande de rendez-vous'})
        if data != -1:
            indexFooter = data.find('<footer>')
            closed_sentence = "Attention : Cette page n'est pas disponible pour le moment !"
            closed = data.find('ultérieurement', 0, indexFooter) != -1 or data.find(closed_sentence, 0,
                                                                                    indexFooter) != -1
            if closed:
                return {"is_open": False, "date": bookingTryDate}
            else:
                writeLog("/!\\ BINGO/!\\")
                return {"is_open": True, "date": bookingTryDate}
        else:
            return {"is_open": False, "date": bookingTryDate}
    else:
        return {"is_open": False, "date": ""}
