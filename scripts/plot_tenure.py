import matplotlib
matplotlib.use('Agg')
import pylab
from django.db.models import Q

from gastronomicus.models import Meeting
from gastronomicus.models import Attendee

def run():

  # PLOT 1
  ##############

  members = Attendee.objects.filter(membership_started__isnull=False,
                                    membership_ended__isnull=False)

  # PLOT 1
  ##############

  members = Attendee.objects.filter(membership_started__isnull=False,
                                    membership_ended__isnull=False)

  print members.count()

  membership_durations = [
      (member.membership_ended - member.membership_started).days / 356.0
      for member in members]

  membership_durations.sort()
  for member in members:
    print member, (member.membership_ended -
                   member.membership_started).days / 356.0

  
  #pylab.hist(membership_durations, cumulative=True, normed=True)
  pylab.hist(membership_durations)
  pylab.title('Histogram of membership duration (years)')
  pylab.ylabel('Number of members')
  pylab.xlabel('Years a member')
  pylab.savefig('membership_duration_histogram.pdf')

  # PLOT 2
  ##############

  guest_attendees = []
  member_attendees = []
  total_attendees = []
  for meeting in Meeting.objects.all():
    num_member_attendees = meeting.attendees.filter(
        membership_started__isnull=False,
        membership_ended__isnull=False).count()
    num_attendees_total = meeting.attendees.count()

    guest_attendees.append(
        (meeting.date, num_attendees_total - num_member_attendees))
    member_attendees.append((meeting.date, num_member_attendees))
    total_attendees.append((meeting.date, num_attendees_total))

  pylab.figure()
  #
  pylab.plot_date(guest_attendees[0], guest_attendees[1])
#             member_attendees, 'g-',
#             total_attendees, 'b-')
  pylab.title('Attendence rates over time')
  pylab.ylabel('Number of attendees')
  pylab.xlabel('Year')
  pylab.savefig('attendence_over_time.pdf')

