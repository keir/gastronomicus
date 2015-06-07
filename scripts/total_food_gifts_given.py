from django.db.models import Q
from gastronomicus.models import Serving
from gastronomicus.models import Meeting

def run():
  # Count total gifts. However, at some meetings a single person brought more
  # than one gift. Count multiple gifts from the same person at the same
  # meeting as only a single gift.
  total_gifts = 0
  for meeting in Meeting.objects.all():
    givers = set()
    for serving in meeting.serving_set.filter(gift=True):
      givers.add(serving.giver)
    total_gifts += len(givers)

  print 'Total gifts given over all meetings:', total_gifts
