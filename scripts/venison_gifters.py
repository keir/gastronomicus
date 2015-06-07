from collections import defaultdict
from gastronomicus.models import Serving
from gastronomicus.models import Meeting

# Top givers:
#
#   Earl of Marchmont Hugh Hume - 88 id: 270
#   Esq. Edward Hooper - 19 id: 403
#   Earl of Morton James Douglas - 14 id: 100
#   Mr. Joseph Banks - 10 id: 530
#   Esq. Charles Stanhope - 10 id: 47
#   Mr. Philip Miller - 9 id: 147
#   Sir William Musgrave - 8 id: 743

#   Earl Phillip York - 33 id: 13
#   Dr. William Heberden - 18 id: 57
#   Earl Shaftesbury - 15 id: 297

ATTENDEE_IDS_OF_INTEREST = set([13, 57, 297])

def run():
  # Print out all the servings for those who tended to give venison.
  for serving in Serving.objects.filter(
      giver__id__in=ATTENDEE_IDS_OF_INTEREST).order_by('meeting__date'):
    print serving

  # Count total gifts. However, at some meetings a single person brought more
  # than one gift. Count multiple gifts from the same person at the same
  # meeting as only a single gift.
  giver_to_year_to_count = defaultdict(lambda: defaultdict(int))
  for meeting in Meeting.objects.all():
    givers = set()
    for serving in meeting.serving_set.filter(gift=True):
      if serving.giver.id in ATTENDEE_IDS_OF_INTEREST:
        givers.add(serving.giver)

    for giver in givers:
      giver_to_year_to_count[giver][meeting.date.year] += 1

  for giver, year_to_count in giver_to_year_to_count.iteritems():
    total_for_giver = 0
    for year in sorted(year_to_count.keys()):
      print giver, year, year_to_count[year]
      total_for_giver += year_to_count[year]
    print 'TOTAL for %s: %s' % (giver, total_for_giver)
