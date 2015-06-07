from gastronomicus.models import Attendee

def run():
  # Dump and count total people who came to the club. 
  for attendee in Attendee.objects.all():
    print attendee

  print 'Total attendees:', Attendee.objects.count()
