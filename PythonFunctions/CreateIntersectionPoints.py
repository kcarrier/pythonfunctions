# ---------------------------------------------------------------------------
# Created on: 2014-09-25
# Modified on: 2014-09-26
# Author: Richard Fairhurst
# Description: This code is designed to create intersection points, end
# points and/or pseudo-node points based on a name/ID attribute that are
# derived from an input line network.  Only line end points are used
# to form intersections, unmatched line ends, or pseudo-nodes.
# High precision topology is typically required to ensure that line ends snap
# together with sufficient accuracy to be considered part of the same
# intersection point.
# ---------------------------------------------------------------------------
"""
I do not take credit for this script but found it useful and it worked for my
use so I thought I would add it to this repository. It is a very intelligent
script and runs extremely fast. Kudos to Richard Fairhurst.
"""

from time import strftime

print "Start script: " + strftime("%Y-%m-%d %H:%M:%S")

import arcpy
from arcpy import env

# Customize the workspace path to fit your data
env.workspace = r"C:\Temp\Intersections\Intersections.gdb"

# Customize the allowWhitespace variable to False to not allow and True
# to allow whitespace or Null names/IDs to be included in the list of
# names/IDs that define the intersection.
allowWhitespace = False

# Customize the name of the field that contains networks line names/IDs
name_field = "FULLNAME"

# Customize the output field names for the line names list, coordinates,
# concatenated coordinates, total line count, and names count list
names_list_field = "STNAMES"
X_field = "X_COORD"
Y_field = "Y_COORD"
XY_field = "LINK_X_Y"
total_count_field = "WAYS_COUNT"
names_count_list_field = "STNAME_WAYS"
point_type_field = "POINT_TYPE"

# Customize the separators for concatenated coordinate keys and lists
opening_separator = "{"
closing_separator = "}"

# Customize the input to your feature class, shapefile or layer
inputdata = r"CENTERLINES"
inputfilefull = env.workspace + "\\" + inputdata

# Customize the output feature class or layer to fit your network
outputfile = r"CL_INTERSECTION_POINTS"
outputfilefull = env.workspace + "\\" + outputfile

# Makes a dictionary of unique string coordinate keys from both line ends
# with values in a list holding a dictionary of intersecting names with
# their counts, coordinates, and a total line count
valueDict = {}
with arcpy.da.SearchCursor(inputdata, [name_field, "SHAPE@"]) as searchRows:
     for searchRow in searchRows:
          name = searchRow[0]
          geometry = searchRow[1]
          From_X = geometry.firstPoint.X
          From_Y = geometry.firstPoint.Y
          To_X = geometry.lastPoint.X
          To_Y = geometry.lastPoint.Y

          # Customize string coordinate keys for the line From and To ends
          # For Latitude and Longitude change the formating below to
          # "%(OSep1)s%(FY)012.8f%(CSep1)s%(OSep2)s%(FX)012.8f%(CSep2)s" % {'OSep1': opening_separator, 'FY': From_Y, 'CSep1': closing_separator, 'OSep2': opening_separator, 'FX': From_X, 'CSep2': closing_separator}
          keyValueFrom = "%(OSep1)s%(FX)012.4f%(CSep1)s%(OSep2)s%(FY)012.4f%(CSep2)s" % {'OSep1': opening_separator, 'FX': From_X, 'CSep1': closing_separator, 'OSep2': opening_separator, 'FY': From_Y, 'CSep2': closing_separator}
          keyValueTo = "%(OSep1)s%(TX)012.4f%(CSep1)s%(OSep2)s%(TY)012.4f%(CSep2)s" % {'OSep1': opening_separator, 'TX': To_X, 'CSep1': closing_separator, 'OSep2': opening_separator, 'TY': To_Y, 'CSep2': closing_separator}

          # Set allowWhitespace to True to include whitespace or Null names
          if allowWhitespace or (len(str(name).strip()) <> 0 and name != None):
               # add new From coordinate into dictionary
               if not keyValueFrom in valueDict:
                    valueDict[keyValueFrom] = [{}, From_X, From_Y, 1]
                    valueDict[keyValueFrom][0][name] = 1
               # add new name into names dictionary of known From coordinate
               elif not name in valueDict[keyValueFrom][0].keys():
                    valueDict[keyValueFrom][0][name] = 1
                    valueDict[keyValueFrom][3] += 1
               # increment counts when the From coordinate and name are known
               else:
                    valueDict[keyValueFrom][0][name] += 1
                    valueDict[keyValueFrom][3] += 1
               # add new To coordinates into dictionary
               if not keyValueTo in valueDict:
                    valueDict[keyValueTo] = [{}, To_X, To_Y, 1]
                    valueDict[keyValueTo][0][name] = 1
               # add new name into names dictionary of known To coordinate
               elif not name in valueDict[keyValueTo][0].keys():
                    valueDict[keyValueTo][0][name] = 1
                    valueDict[keyValueTo][3] += 1
               # increment counts when the To coordinate and name are known
               else:
                    valueDict[keyValueTo][0][name] += 1
                    valueDict[keyValueTo][3] += 1

print "Finished dictionary creation: " + strftime("%Y-%m-%d %H:%M:%S")

# Determine if the outputfilefull exists already
if arcpy.Exists(outputfilefull):
     # Process: Delete outputfilefull...
     arcpy.Delete_management(outputfilefull, "FeatureClass")

# Process: Create Feature Class...
arcpy.CreateFeatureclass_management(env.workspace, outputfile, "POINT", "", "DISABLED", "DISABLED", inputfilefull, "", "0", "0", "0")

# Process: Add names_list_field Field...
arcpy.AddField_management(outputfilefull, names_list_field, "TEXT", "150", "", "150", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add X_field Field...
arcpy.AddField_management(outputfilefull, X_field, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Y_field Field...
arcpy.AddField_management(outputfilefull, Y_field, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add XY_field Field...
arcpy.AddField_management(outputfilefull, XY_field, "TEXT", "", "", "28", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add total_count_field Field...
arcpy.AddField_management(outputfilefull, total_count_field, "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add names_count_list_field Field...
arcpy.AddField_management(outputfilefull, names_count_list_field, "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add names_count_list_field Field...
arcpy.AddField_management(outputfilefull, point_type_field, "TEXT", "", "", "22", "", "NULLABLE", "NON_REQUIRED", "")

print "Finished feature class creation: " + strftime("%Y-%m-%d %H:%M:%S")

# Create an insert cursor for a table specifying the fields that will
# have values provided
fields = [names_list_field, X_field, Y_field, XY_field, total_count_field, names_count_list_field, point_type_field, 'SHAPE@XY']
insertcursor = arcpy.da.InsertCursor(outputfilefull, fields)

# sort the string coordinate keys and process their values
for keyValue in sorted(valueDict.keys()):
     # create a list of names and their counts with separator characters
     # reset variables to hold new lists of names and their counts
     names = ""
     counts = ""
     point_type = ""
     # sort the names dictionary and create the names and counts lists
     for name in sorted(valueDict[keyValue][0].keys()):
          if names == "":
               # Optional: Change separator configuration
               names = opening_separator + str(name) + closing_separator
               counts = opening_separator + str(valueDict[keyValue][0][name]) + closing_separator
          else:
               # Optional: Change separator configuration
               names = names + opening_separator + str(name) + closing_separator
               counts = counts + opening_separator + str(valueDict[keyValue][0][name]) + closing_separator

     if closing_separator + opening_separator in names:
           point_type = "True Intersection"
     elif counts == opening_separator + '1' + closing_separator:
           point_type = "Single-Line End Point"
     elif counts == opening_separator + '2' + closing_separator:
           point_type = "Pseudo Node"
     else:
           point_type = "Branching Lines"

     row = (names, valueDict[keyValue][1], valueDict[keyValue][2], keyValue, valueDict[keyValue][3], counts, point_type, (valueDict[keyValue][1], valueDict[keyValue][2]))
     insertcursor.insertRow(row)

del insertcursor
print "Finished inserting rows: " + strftime("%Y-%m-%d %H:%M:%S")