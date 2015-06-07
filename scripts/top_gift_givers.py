from collections import Counter

from gastronomicus.models import Serving
from gastronomicus.models import Meeting

def run():
  # Count total gifts. However, at some meetings a single person brought more
  # than one gift. Count multiple gifts from the same person at the same
  # meeting as only a single gift.
  giver_to_total_gifts = Counter()
  for meeting in Meeting.objects.all():
    givers = set()
    for serving in meeting.serving_set.filter(gift=True):
      if serving.giver.id == 270:
        print serving
      givers.add(serving.giver)
    giver_to_total_gifts.update(givers)

  # Note that the number for Hugh Hume is inflated due to his re-serving of
  # pickled salmon over subsequent weeks. See the script.
  for giver, number_given in giver_to_total_gifts.most_common(10):
    print giver, '-', number_given

  print 'NOTE: See Hugh Hume script since his true number should be 28.'
