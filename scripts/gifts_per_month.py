import matplotlib
matplotlib.use('Agg')
import pylab

from gastronomicus.models import Attendee
from gastronomicus.models import Meeting
from gastronomicus.models import Serving

# Set default font
import matplotlib.pyplot as plt 
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman')

def run():
  gifts_per_month = [0] * 12

  # Count total gifts. However, at some meetings a single person brought more
  # than one gift. Count multiple gifts from the same person at the same
  # meeting as only a single gift.
  for meeting in Meeting.objects.all():
    givers = set()
    for serving in meeting.serving_set.filter(gift=True):
      givers.add(serving.giver)
    gifts_per_month[meeting.date.month - 1] += len(givers)

  print 'Gifts per month:', gifts_per_month

  pylab.ylim([0, max(gifts_per_month) + 3])

  pylab.bar(left=range(12), height=gifts_per_month, color='#CCCCCC')
  pylab.xticks([0.4 + x for x in range(12)],
               ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec'))
  pylab.title('Total gifts given per month over all meetings')
  pylab.ylabel('Number of gifts')
  pylab.xlabel('Month')
  pylab.savefig('gifts_per_month.pdf')
