from gastronomicus.models import Serving
from gastronomicus.models import Meeting

def run():
  # Hugh Hume gave pickled salmon that would get re-served for subsequent
  # weeks. Compute the number of 'original' salmon gifts, rather than the
  # subsequent reservings.
  total_unique_salmon_gifts = 0

  recently_served_salmon = False
  for meeting in Meeting.objects.all().order_by('date'):

    # Find out if salmon was served at this meeting.
    salmon_serving = None
    for serving in meeting.serving_set.filter(gift=True):
      if serving.giver.id == 270 and serving.dish.name == 'pickled salmon':
        salmon_serving = serving
        break

    if salmon_serving:
      if recently_served_salmon:
        print salmon_serving, 're-served'
        #print salmon_serving.giver, salmon_serving.giver.id
        #serving.gift = False
      else:
        print salmon_serving, '======= FIRST GIFT'
        recently_served_salmon = True
        total_unique_salmon_gifts += 1
    else:
      recently_served_salmon = False

  print 'Total salmon gifts from Hugh Hume:', total_unique_salmon_gifts
