import arcpy
"""
Populate Null, None, Emtpy Strings, or zeros with a message like
No Data Available.
This function will loop over a featureclass and search all fields and replace
the empty values with a message. This is useful for data that might be
publically available where you do not want users seeing Null, None, or blank
values. Assumption is all fields are string/text.
"""

def populatenullvalues():
    # path to featureclass
    fc = 'C:/Temp/temp.gdb/templayer'
    # generate list of all fields
    fields = arcpy.ListFields(fc)
    # the message you want to replace the values with
    msg = 'No Data Available'
    for fld in fields:
        with arcpy.da.UpdateCursor(fc, fld.name) as cursor:
            for row in cursor:
                if row[0] == None or row[0] == "" or row[0] == " " or row[0] == '0':
                    row[0] = msg
                cursor.updateRow(row)

if __name__ == '__main__':
    populatenullvalues()
