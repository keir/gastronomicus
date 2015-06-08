from gastronomicus.models import Serving

def run():
  print 'Meeting date,Dish giver,Dish name,Quantity'
  for serving in Serving.objects.filter(gift=True).order_by('meeting__date'):
    print ','.join(map(str, [serving.meeting.date,
                             serving.giver.name,
                             serving.dish.name,
                             serving.quantity]))
