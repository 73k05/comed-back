import locale
import datetime


# ex: french month == avril return 4
def get_month_from_french(french_month):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    french_month = french_month.lower()

    if french_month == locale.nl_langinfo(locale.MON_1).lower():
        return 1
    if french_month == locale.nl_langinfo(locale.MON_2).lower():
        return 2
    if french_month == locale.nl_langinfo(locale.MON_3).lower():
        return 3
    if french_month == locale.nl_langinfo(locale.MON_4).lower():
        return 4
    if french_month == locale.nl_langinfo(locale.MON_5).lower():
        return 5
    if french_month == locale.nl_langinfo(locale.MON_6).lower():
        return 6
    if french_month == locale.nl_langinfo(locale.MON_7).lower():
        return 7
    if french_month == locale.nl_langinfo(locale.MON_8).lower():
        return 8
    if french_month == locale.nl_langinfo(locale.MON_9).lower():
        return 9
    if french_month == locale.nl_langinfo(locale.MON_10).lower():
        return 10
    if french_month == locale.nl_langinfo(locale.MON_11).lower():
        return 11
    if french_month == locale.nl_langinfo(locale.MON_12).lower():
        return 12

    return 0


def get_date_from_data(data):
    # get the date for dayZero
    # "Semaine du lundi 27 avril 2020 au dimanche 03 mai 2020"
    str_start_date = "Semaine du lundi "
    index_end = data.find(" au dimanche ")

    # Sometimes the response is in English
    if data.find(str_start_date) == -1:
        str_start_date = "Week from lundi "
        index_end = data.find(" to dimanche ")

    index_start = data.find(str_start_date) + len(str_start_date)
    day_of_the_month = data[index_start:index_start + 2]
    # "Semaine du lundi 27 [avril 2020] au dimanche 03 mai 2020"
    str_month_and_year = data[index_start + 3:index_end]
    size_month_year = len(str_month_and_year)
    # Remove 4 because the year is always on 4 digit ex: 2020 so it's isolates 2020 from "Avril 2020"
    month_french = str_month_and_year[:size_month_year - 5]
    year = str_month_and_year[size_month_year - 4:size_month_year]
    month = get_month_from_french(month_french)
    # then dayBooking - dayZero % 7 and request again
    return datetime.datetime(int(year), int(month), int(day_of_the_month))


# Update index to reach today's date
def update_index_day_zero_to_today(index_day_zero, date_zero, date_today):
    days_in_week = 7
    while date_zero + datetime.timedelta(days=-days_in_week) < date_today:
        date_zero = date_zero + datetime.timedelta(days=days_in_week)
        index_day_zero += days_in_week
    while date_zero > date_today:
        date_zero = date_zero + datetime.timedelta(days=-days_in_week)
        index_day_zero -= days_in_week
    if index_day_zero < 0:
        index_day_zero = 0
    return index_day_zero


def string_to_date(date_string_value):
    if not date_string_value:
        return None
    return datetime.datetime.strptime(date_string_value, '%d/%m/%Y')

