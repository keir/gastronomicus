import json
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import pylab

from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response

from gastronomicus.models import Meeting
from gastronomicus.models import Attendee

def members(attendee_qs):
    return attendee_qs.filter(
            membership_started__isnull=False,
            membership_ended__isnull=False)

def compute_adjacency():
    def order(a, b):
        'Swap a and b to ensure a.id < b.id'
        if b.id < a.id:
            return b, a
        return a, b

    weights = defaultdict(int)
    num_skipped = 0
    for meeting in Meeting.objects.all():
        if meeting.date.year > 1780:
            num_skipped += 1
            continue
        print meeting
        #attendees = list(set(meeting.attendees.all()))
        attendees = list(set(members(meeting.attendees).all()))
        #print 'all %s members %s' % (
        #        meeting.attendees.all().count(),
        #        members(meeting.attendees).count())
        for i in range(len(attendees)):
            for j in range(i + 1, len(attendees)):
                a, b = order(attendees[i], attendees[j])
                assert a != b
                weights[(a.id, b.id)] += 1

    # This is the format expected by mbostock's adjancency visualizer.
    links = [dict(source=source_id, target=target_id, value=value)
             for (target_id, source_id), value in weights.iteritems()]

    print 'Got %s total links' % len(links)

    # Sort by strength so we can discard "weak" links entirely. Take the top
    # 100 for now; later on figure out a better way to slice and dice.
    links.sort(key=lambda link: link['value'], reverse=True)

    print 'Exporting to CSV...'
    f = open('coocurrences.csv', 'w')
    for link in links:
        f.write('%s,%s,%s\n' % (
                Attendee.objects.get(id=link['source']).name,
                Attendee.objects.get(id=link['target']).name,
                link['value']))
    f.close()

    print 'Skipped: ', num_skipped

    pylab.plot([link['value'] for link in links], 'r.')
    pylab.ylabel('Number of co-attendences')
    pylab.xlabel('Co-occurence (sorted by rank)')
    pylab.savefig('cooccurence_dropoff.pdf')


    attendees_in_links = Attendee.objects.filter(
            id__in=(set(link['source'] for link in links) |
                    set(link['target'] for link in links)))
    nodes = [dict(name=attendee.name, group=1, id=attendee.id)
             for attendee in attendees_in_links]

    # Unfortunately the source/target numbers should not be DB IDs but instead
    # should be indices into the earlier graph. So remap all the IDs.
    id_to_index_map = {attendee['id'] : i for i, attendee in enumerate(nodes)}
    for link in links:
        link['source'] = id_to_index_map[link['source']]
        link['target'] = id_to_index_map[link['target']]

    return dict(links=links, nodes=nodes)

def adjacency(request):
    return HttpResponse(json.dumps(compute_adjacency(), indent=2),
                        mimetype='text/json')

#def my_view(request):
#    return render_to_response('myapp/index.html', {"foo": "bar"},
#        mimetype="application/xhtml+xml")

def home(request):
    return render_to_response('templates/index.html', mimetype="text/html")
