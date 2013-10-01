import matplotlib
matplotlib.use('Agg')
import pylab

from datetime import date

from django.db.models import Q
from numpy import *
from collections import defaultdict

from gastronomicus.models import Meeting
from gastronomicus.models import Attendee
from gastronomicus.models import Serving
from gastronomicus.models import Dish

def summarize(x):
  print 'Mean', sum(x) / float(len(x))
  print 'Standard Deviation', std(x)
  print 'Max', max(x)
  print 'Min', min(x)
  print 'Entries', len(x)

def members(attendee_qs):
    return attendee_qs.filter(
            membership_started__isnull=False,
            membership_ended__isnull=False)

def attendence_count_histogram():
  counts = defaultdict(int)
  for meeting in Meeting.objects.all():
    for attendee in set(meeting.attendees.all()):
      counts[attendee] += 1

  # This is the format expected by mbostock's adjancency visualizer.
  histogram = list(reversed(sorted(
      [(count, attendee) for (attendee, count) in counts.iteritems()])))

  for count, attendee in histogram[:200]:
    print '%10s   %s' % (count, attendee)

def num_attended(attendee):
  attended = 0
  for meeting in Meeting.objects.all():
    if meeting.attendees.filter(id=attendee.id):
      attended += 1
  return attended

def election_attendence_table():
  attendence = defaultdict(int)
  for meeting in Meeting.objects.all():
    if meeting.date.month != 7: # july
      continue
    if meeting.date.day + 7 <= 31:
      continue

    print 'Date of election:', meeting.date

    for attendee in meeting.attendees.all():
      attendence[attendee.name] += 1

  attendence = sorted([(count, attendee)
                       for (attendee, count) in attendence.iteritems()])
  for record in attendence:
    print '%s,%s' % record

def vetting_process():
  all_members = set(members(Attendee.objects.all()))
  times_attended_before_member = defaultdict(int)
  earliest_year_attended = {}

  for meeting in Meeting.objects.all():
    for attendee in members(meeting.attendees):
      if meeting.date < attendee.membership_started:
        times_attended_before_member[attendee] += 1
        earliest_year_attended[attendee] = min(
            earliest_year_attended.get(attendee, date.today()),
            meeting.date)

  times_attended_before_member = reversed(sorted(
      [(count, attendee)
       for (attendee, count)
       in times_attended_before_member.iteritems()]))
  for count, attendee in times_attended_before_member:
    time_before_member = (attendee.membership_started -
                          earliest_year_attended[attendee])
    print '%s,%s,%s' % (count, attendee.name, round(time_before_member.days / 365.0, 1))

def gifted_per_year(match, name, make_hist=False):
  if False:
    year_to_count = defaultdict(int)
    for serving in set(Serving.objects.all()):
      if match(serving.dish.name):
        print serving.dish.name
        year_to_count[serving.meeting.date.year] += 1

  # Only count one match per meeting.
  year_to_count = defaultdict(int)
  for meeting in Meeting.objects.all():
    for dish in meeting.servings.all():
      if match(dish.name):
        print dish.name
        year_to_count[meeting.date.year] += 1
        break

  years = year_to_count.keys()
  counts = year_to_count.values()

  print 'Total:', sum(counts)

  pylab.hist(counts)
  pylab.title('Histogram of amount of %s served per year' % name)
  pylab.ylabel('Number of years with that number of servings')
  pylab.xlabel('Number of times %s was served' % name)
  pylab.savefig('servings_per_year_%s_hist.pdf' % name)

  pylab.figure()
  pylab.plot(years, counts, 'r.')
  pylab.title('Amount of %s served per year' % name)
  pylab.ylabel('Number of servings')
  pylab.xlabel('Year')
  pylab.savefig('servings_per_year_%s.pdf' % name)

def gifted_per_year_multiple(match_and_names):
  for match, name, style in match_and_names:
    # Only count one match per meeting.
    year_to_count = defaultdict(int)
    for meeting in Meeting.objects.all():
      for dish in meeting.servings.all():
        if match(dish.name):
          print dish.name
          year_to_count[meeting.date.year] += 1
          break

    years = year_to_count.keys()
    counts = year_to_count.values()

    print 'Total for %s: %s' % (name, sum(counts))

    pylab.plot(years, counts, style, label=name)

  print 'Writing fancy_dish_servings_per_year.pdf...'
  pylab.title('Venison and turtle dinners')
  pylab.ylabel('Number of dinners with the dish')
  pylab.xlabel('Year')
  pylab.legend()
  pylab.savefig('fancy_dish_servings_per_year.pdf')

def histogram_of_number_of_attendees():
  num_attendees = [meeting.attendees.all().count()
                   for meeting in Meeting.objects.all()]
  num_attendees = filter(None, num_attendees)

  pylab.hist(num_attendees)
  pylab.title('Histogram of number of attendees in each meeting')
  pylab.ylabel('Number of meetings')
  pylab.xlabel('Number of attendees')
  print 'Writing num_attendees_hist.pdf...'
  pylab.savefig('num_attendees_hist.pdf')

def quantize_date(a_date):
  # Quantize to month for now.
  return date(a_date.year, a_date.month, 1)

def attendence_numbers_over_time():
  # Accumulate stats per period (month) over each meeting.
  data = {}
  for meeting in Meeting.objects.all():
    num_members = meeting.attendees.filter(
        membership_started__isnull=False,
        membership_ended__isnull=False).count()

    if num_members == 0:
      print 'No members: %s; id=%s' % (meeting, meeting.id)
      continue

    num_attendees = meeting.attendees.count()
    num_guests = num_attendees - num_members

    quantized_date = quantize_date(meeting.date)
    data_for_block = data.get(quantized_date, defaultdict(int))
    data_for_block['num_member'] += num_members
    data_for_block['num_total'] += num_attendees
    data_for_block['num_guests'] += num_guests
    data[quantized_date] = data_for_block

  data = sorted(data.items(), key=lambda x: x[0])

  print 'bSTNHSNTHSNTH'
  for x in data[:50]:
    print x[0], x[1]
  print '--bSTNHSNTHSNTH'

  dates = matplotlib.dates.date2num(item[0] for item in data)
  num_members = [item[1]['num_member'] for item in data]
  num_guests = [item[1]['num_guests'] for item in data]

  pylab.plot_date(dates, num_members, 'b.', label='Members')
  pylab.plot_date(dates, num_guests, 'r.', label='Guests')
  pylab.title('Number of attendees over time')
  pylab.ylabel('Number of attendees per month')
  pylab.xlabel('Date of meeting')
  pylab.legend()
  print 'Writing num_attendees_over_time.pdf...'
  pylab.savefig('num_attendees_over_time.pdf')

def run():
  #election_attendence_table()
  #vetting_process()
  #histogram_of_number_of_attendees()
  #attendence_numbers_over_time()
  #return

  #gifted_per_year(lambda x: x in ('turtle', 'calapash'), 'turtle', make_hist=True)
  #gifted_per_year(lambda x: 'venison' in x, 'venison', make_hist=True)

  # Note: The 7-year war split! Cool split in the data
  #gifted_per_year(lambda x: 'roast beef' in x, 'roast_beef', make_hist=True)

  # Not as interesting.
  #gifted_per_year(lambda x: ('ragout' in x or 'fricassee' in x),
  #                'ragout', make_hist=True)

  #gifted_per_year(lambda x: ('calves head' in x), 'calves_head', make_hist=True)

  #gifted_per_year(lambda x: ('mock turtle' in x), 'mock_turtle')

  gifted_per_year_multiple([
      (lambda x: x in ('turtle', 'calapash'), 'Turtle', 'go'),
      (lambda x: 'venison' in x, 'Venison', 'rd')
      ])

  #gifted_per_year(lambda x: 'mock turtle' in x, 'mock_turtle')
  return
  #attendence_count_histogram()
  #return

  # Highest attendance to a club dinner
  member_attendees = []
  total_attendees = []
  total_dishes = []
  ratio_guests_to_members = []
  for meeting in Meeting.objects.all():
    num_member_attendees = meeting.attendees.filter(
        membership_started__isnull=False,
        membership_ended__isnull=False).count()
    if num_member_attendees == 0:
      print 'No members: %s; id=%s' % (meeting, meeting.id)
      continue
    num_attendees_total = meeting.attendees.count()

    member_attendees.append(num_member_attendees)
    total_attendees.append(num_attendees_total)
    total_dishes.append(meeting.servings.count())

    num_guests = num_attendees_total - num_member_attendees

    ratio_guests_to_members.append(num_guests / float(num_member_attendees))

  member_attendees = array(member_attendees)
  total_attendees = array(total_attendees)
  guest_attendees = total_attendees - member_attendees

  print
  print 'Summary stats for members'
  summarize(member_attendees)

  print
  print 'Summary stats for guests'
  summarize(guest_attendees)
  
  print
  print 'Summary stats for total attendees'
  summarize(total_attendees)

  print
  print 'Summary stats for dishes per meeting'
  summarize(total_dishes)

  print
  print 'Summary stats for ratio of guests to members'
  summarize(ratio_guests_to_members)

  #max_attendence_meeting = Meeting.objects.order_by('-attendees__count')[0]
  #print 'Max attendees:', max_attendence_meeting.attendees

  # Dishes with beef
#  for dish in Dish.objects.all():
#    if 'beef' in dish.name:
#      print dish

  # Colebrook - id 11
  # Birch - id 20
#  for attendee in Attendee.objects.all():
#    if 'Birch' in attendee.last_name:
#      print 'Got:', attendee, attendee.id
  #print 'Colebrook attended:', num_attended(Attendee.objects.get(id=11))
#  print 'Birch attended:', num_attended(Attendee.objects.get(id=20))



