from django import template
from xformmanager.models import *
from hq.models import *
from hq.models import *
register = template.Library()
from resources.models import *
from facilities.models import Facility

xmldate_format= '%Y-%m-%dT%H:%M:%S'
output_format = '%Y-%m-%d %H:%M'

def _get_class(count):
    if count % 2 == 0:
        return "even"
    return "odd"

def _getsamples(day,month,year,area):
    
    check = int(area)
    if check == 0:
        samples = Resource.objects.filter(date_added__day = day,
                            date_added__month = month,
                            date_added__year = year,
                            )
    else:
        a = Resource.objects.filter(  date_added__day = day,
                                            date_added__month = month,
                                            date_added__year = year)
        samples = a.filter(facility__id = area)
    return samples


@register.simple_tag
def get_samples(day,month,year,area):
    samples = _getsamples(day,month,year,area)

    ret = ''
    ret += '''<table>\n<thead><tr>
            <th>Date Added</th>
            <th>Name</th>
            <th>Code</th>
            <th>Facility</th>
            <th>Status</th></tr></thead><tbody>'''
    count = 1
    if samples:
        for sample in samples:
                ret += '\n<tr class="%s">' % _get_class(count)
                count += 1
                ret += '<td>%s-%s-%s</td>' % ( sample.date_added.day, sample.date_added.month, sample.date_added.year)
                ret += '<td>%s</td>' % (sample.name)
                ret += '<td>%s</td>' % (sample.code)
                ret += '<td>%s</td>' % (sample.facility)
                ret += '<td>%s</td>' % (sample.status)
    else:
        ret += '<td>No samples submitted</td>'
    ret += '</tbody></table>'
    return ret
