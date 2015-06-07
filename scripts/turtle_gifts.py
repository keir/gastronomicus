from gastronomicus.models import Serving
from gastronomicus.models import Meeting

def run():
  # Note that some of these seem to miss a gift giver (turtle was rare!)
  for serving in Serving.objects.all().order_by('meeting__date'):
    if serving.dish.name == 'turtle':
      print serving
