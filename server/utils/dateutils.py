import locale
import datetime


# ex: frenchmonth == avril return 4
def getmonthfromfrench(frenchmonth):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    frenchmonth = frenchmonth.lower()

    if frenchmonth == locale.nl_langinfo(locale.MON_1).lower():
        return 1
    if frenchmonth == locale.nl_langinfo(locale.MON_2).lower():
        return 2
    if frenchmonth == locale.nl_langinfo(locale.MON_3).lower():
        return 3
    if frenchmonth == locale.nl_langinfo(locale.MON_4).lower():
        return 4
    if frenchmonth == locale.nl_langinfo(locale.MON_5).lower():
        return 5
    if frenchmonth == locale.nl_langinfo(locale.MON_6).lower():
        return 6
    if frenchmonth == locale.nl_langinfo(locale.MON_7).lower():
        return 7
    if frenchmonth == locale.nl_langinfo(locale.MON_8).lower():
        return 8
    if frenchmonth == locale.nl_langinfo(locale.MON_9).lower():
        return 9
    if frenchmonth == locale.nl_langinfo(locale.MON_10).lower():
        return 10
    if frenchmonth == locale.nl_langinfo(locale.MON_11).lower():
        return 11
    if frenchmonth == locale.nl_langinfo(locale.MON_12).lower():
        return 12

    return 0


def getdatefromdata(data):
    # get the date for dayZero
    # "Semaine du lundi 27 avril 2020 au dimanche 03 mai 2020"
    strStartDate = "Semaine du lundi "
    if data.find(strStartDate) == -1:
        strStartDate = "Week from lundi "
        indexEnd = data.find(" to dimanche ")
        indexStart = data.find(strStartDate) + len(strStartDate)
    else:
        indexStart = data.find(strStartDate) + len(strStartDate)
        indexEnd = data.find(" au dimanche ")

    dayOfTheMonth = data[indexStart:indexStart + 2]
    # "Semaine du lundi 27 [avril 2020] au dimanche 03 mai 2020"
    strMonthAndYear = data[indexStart + 3:indexEnd]
    sizeMonthYear = len(strMonthAndYear)
    # Remove 4 because the year is always on 4 digit ex: 2020 so it's isolates 2020 from "Avril 2020"
    monthFrench = strMonthAndYear[:sizeMonthYear - 5]
    year = strMonthAndYear[sizeMonthYear - 4:sizeMonthYear]
    month = getmonthfromfrench(monthFrench)
    # then dayBooking - dayZero % 7 and request again
    return datetime.datetime(int(year), int(month), int(dayOfTheMonth))


# Update index to reach today's date
def update_index_day_zero_to_today(indexDayZero, dateZero, dateToday):
    while dateZero < dateToday:
        dateZero = dateZero + datetime.timedelta(days=7)
        indexDayZero += 7
    return indexDayZero
