from gastronomicus.models import Attendee
from gastronomicus.models import Serving

def run():
  # Find all the attendees who gave gifts. There is likely a better way to do
  # this with the ORM, but whatever.
  giver_ids = set()
  for serving in Serving.objects.filter(gift=True):
    giver_ids.add(serving.giver)

  givers = len(giver_ids)
  total = Attendee.objects.all().count()

  print 'Total givers:', givers
  print 'Total attendees:', total
  print 'Percent of givers: %0.2f%%' % (float(givers) / total * 100)
