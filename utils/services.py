import datetime


def date_between(start_date, end_date):
    """
    Generate an iterator of dates between the two given dates.
    taken from http://stackoverflow.com/questions/1060279/
    """
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + datetime.timedelta(n)

def months_between(start_date, end_date):
    """
    Given two instances of ``datetime.date``, generate a list of dates on
    the 1st of every month between the two dates (inclusive).

    e.g. "5 Jan 2020" to "17 May 2020" would generate:

        1 Jan 2020, 1 Feb 2020, 1 Mar 2020, 1 Apr 2020, 1 May 2020

    """
    year = start_date.year
    month = start_date.month
    while (year, month) <= (end_date.year, end_date.month):
        yield datetime.date(year, month, 1)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

def years_between(start_date, end_date):
    """
    Given two instances of ``datetime.date``, generate a list of dates on
    the 1st of every year between the two dates (inclusive).

    e.g. "5 Jan 2020" to "17 May 2020" would generate:

        1 Jan 2020, 1 Feb 2020, 1 Mar 2020, 1 Apr 2020, 1 May 2020

    """
    year = start_date.year

    while (year) <= (end_date.year):
        yield datetime.date(year, 1, 1)
        year += 1