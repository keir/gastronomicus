from collections import Counter, defaultdict
from gastronomicus.models import Serving
from gastronomicus.models import Meeting

category_to_dishes = {
  'turtle': ['turtle', 'callipash'],
  'game': [
      'brace of hare',
      'brace of hares',
      'brace of partridges',
      'brace of pheasants',
      'hare',
      'partridges',
      'pheasants',
      'roast fowles',
      ],
  'pickled salmon': ['pickled salmon'],
  'other fish': [
      'brace of carp',
      'carp',
      'flat fish and pike',
      'lampreys',
      'newcastle salmon',
      'perch and whitings',
      'pike',
      'pikes and soles',
      'potted charr',
      'salmon',
      'turbot',
      'tusk',
      ],
  'fresh fruit': [
      'apricots',
      'cantaloupe',
      'cherry',
      'currants',
      'fruit',
      'gooseberries',
      'grapes',
      'melon',
      'peaches',
      'pear',
      'pinapple',
      'pineapple',
      'plum',
      'plums',
      'rasberries',
      'stewed melon',
      'strawberries',
      'strawberry',
      'water melon',
      ],
  'exotic vegtables': [
      'egyption lettuce',
      'coss lettuces',
      'lettuces'
      ],
  'beef': [
      'beef',
      'chine of beef',
      'achbone of beef'
      ],
  'venison': [
      'haunch of venison',
      'venison',
      'venison pye',
      'neck of venison',
      'neck of roast venison',
      'haunch of roast venison',
      'venison pasty', 'roast fawn'
      ],
  'other': ['china pig', 'roast pig']
}

dish_to_category = {}
for category, dishes in category_to_dishes.iteritems():
  for dish in dishes:
    dish_to_category[dish] = category


def run():
  category_counts = Counter()

  # Count the amount of gifts in each category, but only count one gift per
  # person per category per meeting (e.g. if Hugh Hume gave both partridges and
  # pheasant in one meeting, count it as only one gift)
  for meeting in Meeting.objects.all():
    giver_to_categories_given = defaultdict(set)
    for serving in meeting.serving_set.filter(gift=True):
      giver_to_categories_given[serving.giver].add(
          dish_to_category[serving.dish.name])
    for categories in giver_to_categories_given.values():
      category_counts.update(categories)

  # Note that the pickled salmon number is off due to Hugh Hume.
  for category, count in category_counts.iteritems():
    print category, count
