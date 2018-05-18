import arcpy, datetime
"""
The function finddatenextday will return the next possible date for a given
weekday.

The goal was to find the actual dates for the next occurence of the weekday.

The function trashscheduledate is using an update cursor and looping over the
values in the TrashSchedule field which is populated with days of the week as
strings Monday, Tuesday, etc... It then calls the finddatenextday function and
returns an easy to read date for the next occurence of that weekday. So if you
are looking for a way to populate the next available date based on a string like
'Monday' then you could use the finddatenextday function to do so.
"""

def finddatenextday(x):
    timelst = []
    today = findlastsaturday()
    nextday = today + datetime.timedelta( (x-today.weekday()) % 7 )
    timelst.append(nextday)
    easydate = timelst[0].strftime('%m-%d-%Y')
    return easydate

def trashscheduledate():
    fc = 'C:/Temp/temp.gdb/TrashScheduleLayer'
    fields = ['TrashSchedule', 'TrashScheduleDate']

    # Create update cursor for feature class
    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        # For each row, evaluate the TrashSchedule value, and update
        # TrashScheduleDate with an easy to read date value.

        for row in cursor:
            if (row[0] == 'Monday'):
                row[1] = finddatenextday(0) # 0 = Monday
            if (row[0] == 'Tuesday'):
                row[1] = finddatenextday(1) # 1 = Tuesday
            if (row[0] == 'Wednesday'):
                row[1] = finddatenextday(2) # 2 = Wednesday
            if (row[0] == 'Thursday'):
                row[1] = finddatenextday(3) # 3 = Thursday
            if (row[0] == 'Friday'):
                row[1] = finddatenextday(4) # 4 = Friday
            if (row[0] == 'Saturday'):
                row[1] = finddatenextday(5) # 5 = Saturday
            if (row[0] == 'Sunday'):
                row[1] = finddatenextday(6) # 6 = Sunday

            # Update the cursor with the updated list
            cursor.updateRow(row)

if __name__ == '__main__':
    trashscheduledate()
