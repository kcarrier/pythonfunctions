import datetime, calendar

"""
Developed so that if you have a script which does not run as expected on a
specified day and you are dealing with dates, then you want to make the script
act like it is running on that day. For example a script runs on Saturday but
you come in Monday only to find there was an error or problem. You need the code
to execute as though it is still the previous Saturday so the dates populate
correctly.
"""

def findlastsaturday():
    # get today's date
    now = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    # find the previous day of the week, replace SATURDAY with whatever
    # weekday you are looking to get a date for
    if now.weekday() != calendar.SATURDAY:
        while now.weekday() != calendar.SATURDAY:
            now -= oneday
    return now

if __name__ == '__main__':
    lastsaturday = findlastsaturday()
    print(lastsaturday)
