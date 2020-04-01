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


def getParamsFromUser(userJson):
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
