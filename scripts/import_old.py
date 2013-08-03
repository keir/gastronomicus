import os
import time
from datetime import datetime

import sqlite3

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from gastronomicus.models import Attendee
from gastronomicus.models import Dish
from gastronomicus.models import Meeting
from gastronomicus.models import Attendee
from gastronomicus.models import Serving

'''
CREATE TABLE "tblClubMeeting"(
  "MeetingID" INTEGER  NOT NULL PRIMARY KEY,
  "DateString" VARCHAR(255),
  "DateMonth" INTEGER,
  "DateDay" INTEGER,
  "DateYear" INTEGER,
  "AttendanceMembers" INTEGER,
  "AttendanceGuests" INTEGER,
  "AttendanceTotal" INTEGER,
  "TreasurersComments" LONGVARCHAR,
  "IndiasComments" LONGVARCHAR
);

CREATE TABLE "tblDish"(
  "DishID" INTEGER  NOT NULL PRIMARY KEY,
  "DishName" VARCHAR(255)
);

CREATE TABLE "tblDishMeetingJunc"(
  "DishID" INTEGER NOT NULL,
  "MeetingID" INTEGER NOT NULL,
  "Quantity" INTEGER,
  "GiftBoolean" INTEGER,
  "GiftGiverMenID" INTEGER,
  PRIMARY KEY("DishID","MeetingID"),
  FOREIGN KEY("MeetingID") REFERENCES "tblClubMeeting"("MeetingID"),
  FOREIGN KEY("DishID") REFERENCES "tblDish"("DishID")
);

CREATE TABLE "tblMen"(
  "MenID" INTEGER  NOT NULL PRIMARY KEY,
  "Membership" INTEGER,
  "DateAdmittedYear" INTEGER,
  "MenFirstName" VARCHAR(50),
  "MenLastName" VARCHAR(50),
  "MenTitle" VARCHAR(50),
  "MenNotes" LONGVARCHAR,
  "DateEndYear" INTEGER
);

CREATE TABLE "tblMenMeetingJunc"(
  "MeetingID" INTEGER NOT NULL,
  "MenID" INTEGER NOT NULL,
  PRIMARY KEY("MeetingID","MenID"),
  FOREIGN KEY("MeetingID") REFERENCES "tblClubMeeting"("MeetingID"),
  FOREIGN KEY("MenID") REFERENCES "tblMen"("MenID")
);

'''

# From https://en.wikipedia.org/wiki/Julian_day
def julian_calendar_date_to_julian_day_number(year, month, day):
  a = (14 - month) / 12
  y = year + 4800 - a
  m = month + 12 * a - 3
  return day + (153 * m) / 5 + 365 * y + y / 4 - 32083

def julian_date_to_gregorian_date(year, month, day):
  julian_day_number = julian_calendar_date_to_julian_day_number(year,
                                                                month,
                                                                day)
  return jd2gd(julian_day_number)

# Adapted from:
# http://www.astro.ucla.edu/~ianc/python/_modules/date.html
def jd2gd(jd):
    """Task to convert a julian date to a gregorian date.
    Description at http://mathforum.org/library/drmath/view/51907.html
    Original algorithm in Jean Meeus, "Astronomical Formulae for
    Calculators"

    2009-02-15 13:36 IJC: Converted to importable, callable function
    """
    jd=jd+0.5
    Z=int(jd)
    F=jd-Z
    alpha=int((Z-1867216.25)/36524.25)
    A=Z + 1 + alpha - int(alpha/4)

    B = A + 1524
    C = int( (B-122.1)/365.25)
    D = int( 365.25*C )
    E = int( (B-D)/30.6001 )

    dd = B - D - int(30.6001*E) + F

    if E<13.5:
	mm=E-1

    if E>13.5:
	mm=E-13

    if mm>2.5:
	yyyy=C-4716

    if mm<2.5:
	yyyy=C-4715

    months=[ "January",
             "February",
             "March",
             "April",
             "May",
             "June",
             "July",
             "August",
             "September",
             "October",
             "November",
             "December"]
    daylist=[31,28,31,30,31,30,31,31,30,31,30,31]
    daylist2=[31,29,31,30,31,30,31,31,30,31,30,31]

    h=int((dd-int(dd))*24)
    min=int((((dd-int(dd))*24)-h)*60)
    sec=86400*(dd-int(dd))-h*3600-min*60

    # Now calculate the fractional year. Do we have a leap year?
    if (yyyy%4 != 0):
	days=daylist2
    elif (yyyy%400 == 0):
	days=daylist2
    elif (yyyy%100 == 0):
	days=daylist
    else:
	days=daylist2

    hh = 24.0*(dd % 1.0)
    min = 60.0*(hh % 1.0)
    sec = 60.0*(min % 1.0)

    dd =  dd-(dd%1.0)
    hh =  hh-(hh%1.0)
    min =  min-(min%1.0)

    return (int(yyyy), int(mm), int(dd))

# The original database has several typos; correct them.
typos =  {
  'deceber': 'december',
  'ferbuary': 'february',
  'jaunary': 'january',
  'marhc'    : 'march',
  'nobember' : 'november',
  'ocober'   : 'october',
  'septeber': 'september',
  'septemer': 'september',
}

def run():
    connection = sqlite3.connect('old.db')
    connection.row_factory = sqlite3.Row # Get dictionaries instead of tuples.
    print 'Running conversion...'
    print os.getcwd()

    # Convert the men into attendees.
    for row in connection.execute('SELECT * FROM tblMen'):
        attendee = Attendee()
        attendee.id = row['MenID']
        if row['DateAdmittedYear']:
            attendee.membership_started = datetime(
                    int(row['DateAdmittedYear']), 1, 1)
            print 'started', attendee.membership_started

        if row['DateEndYear']:
            attendee.membership_started = datetime(
                    int(row['DateEndYear']), 1, 1)
            print 'ended', attendee.membership_ended

        if row['MenFirstName'] and row['MenFirstName'] != 'na':
            attendee.first_name = row['MenFirstName']

        if row['MenLastName'] and row['MenLastName'] != 'na':
            attendee.last_name = row['MenLastName']

        if row['MenTitle']:
            attendee.title = row['MenTitle']

        if row['MenNotes']:
            attendee.notes = row['MenNotes']
        
        print 'Attendee -', attendee

        attendee.save()

    # Convert the dishes into dishes.
    for row in connection.execute('SELECT * FROM tblDish'):
        dish = Dish()
        dish.id = row['DishID']
        dish.name = row['DishName']
        print 'Dish -', dish

        dish.save()

    # Convert the meetings into meetings.
    Meeting.objects.all().delete()
    for row in connection.execute('SELECT * FROM tblClubMeeting'):
        meeting_id = row['MeetingID']
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except ObjectDoesNotExist:
            meeting = Meeting()
            meeting.id = row['MeetingID']

        parsed_date = None
        def error():
            print ('http://localhost:8000/admin/gastronomicus/meeting/%s/' %
                   meeting.id)

        if row['DateString']:
            date_string = row['DateString'].replace(',', ' ').lower()
            date_string = ' '.join(date_string.split())
            date_string = date_string.replace('*', '')
            date_string = date_string.replace('/9', '')
            date_string = date_string.replace('/1', '')

            # Fix the typos.
            if date_string.split()[0] in typos:
              exploded = date_string.split()
              date_string = ' '.join([typos[exploded[0]]] + exploded[1:])

            try:
                parsed_date = datetime.strptime(date_string, '%B %d %Y')
            except ValueError:
                error()
                print 'ERROR: Could not parse: %s' % date_string

        composed_date = datetime(row['DateYear'],
                                 row['DateMonth'],
                                 row['DateDay'])

        if (composed_date and parsed_date and
            composed_date != parsed_date):
            error()
            print 'Dates do not match. Composed: %s, Parsed %s' % (
                    composed_date, parsed_date)

        date = composed_date

        if date < datetime(1752, 8, 27):
            # This is a Julian date that needs converting to Gregorian.
            #print 'Converting Julian date:', date
            date = datetime(*julian_date_to_gregorian_date(date.year,
                                                           date.month,
                                                           date.day))

        meeting.date = date

        if row['TreasurersComments']:
            meeting.treasurer_comments = row['TreasurersComments']

        if row['IndiasComments']:
            meeting.comments = row['IndiasComments']

        try:
            meeting.save()
        except IntegrityError:
            print 'Integrity error! date:', date
            print 'ID of offending object', meeting.id
            print 'Ignoring!'

    # Convert the meeting junction into servings.
    for row in connection.execute('SELECT * FROM tblDishMeetingJunc'):
        serving = Serving()
        serving.dish = Dish.objects.get(id=int(row['DishID']))
        meeting_id = int(row['MeetingID'])
        if meeting_id == 820:
          # India made two meeting (upstairs and downstairs); merge them instead.
          meeting_id = 819

        serving.meeting = Meeting.objects.get(id=meeting_id)
        # Force a deterministic ID for the import, so it is possible to run the
        # import multiple times.
        serving.id = 10000 * serving.meeting.id + serving.dish.id
        if row['Quantity']:
            try:
                serving.quantity = int(row['Quantity'])
            except ValueError:
                print 'ERROR: Not an integer:', row['Quantity']
                print 'Meeting ID:', serving.meeting.id
                print 'Dish ID:', serving.dish.id

        if row['GiftBoolean']:
            # XXX should this be stringified?
            #print 'gift boolean:', repr(row['GiftBoolean'])
            serving.gift = bool(row['GiftBoolean'])

        if row['GiftGiverMenID']:
            serving.giver = Attendee.objects.get(id=int(row['GiftGiverMenID']))

        serving.save()
            
    # Convert the meeting junction into servings.
    for row in connection.execute('SELECT * FROM tblMenMeetingJunc'):
        meeting_id = int(row['MeetingID'])
        if meeting_id == 820:
            # India made two meetings (upstairs and downstairs) for this date;
            # merge them instead.
            meeting_id = 819
        meeting = Meeting.objects.get(id=meeting_id)
        attendee = Attendee.objects.get(id=int(row['MenID']))
        meeting.attendees.add(attendee)

        meeting.save()

# Meeting
