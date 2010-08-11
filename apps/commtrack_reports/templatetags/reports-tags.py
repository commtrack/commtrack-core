from django import template
from xformmanager.models import *
from hq.models import *
from hq.models import *
register = template.Library()

xmldate_format= '%Y-%m-%dT%H:%M:%S'
output_format = '%Y-%m-%d %H:%M'

def _get_class(count):
    if count % 2 == 0:
        return "even"
    return "odd"


@register.simple_tag
def get_samples(samples):
    ret = ''
    ret += '''<table>\n<thead><tr>
            <th>Domain</th>
            <th>Facility</th>
            <th>Name</th>
            <th>Date</th>
            <th>Code</th>
            <th>Status</th></tr></thead><tbody>'''
    count = 1
    month_names = ['0','jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    if samples:
        for sample in samples:
                ret += '\n<tr class="%s">' % _get_class(count)
                count += 1
                ret += '<td>%s</td>' % (sample.facility.domain)
                ret += '<td>%s</td>' % (sample.facility)
                ret += '<td>%s</td>' % (sample.name)
                month_name = month_names[sample.date_added.month]
                ret += '<td>%s-%s-%s</td>' % ( sample.date_added.day,month_name , sample.date_added.year)
                ret += '<td>%s</td>' % (sample.code)
                ret += '<td>%s</td>' % (sample.status)
    else:
        ret += '<td>No samples submitted</td>'
    ret += '</tbody></table>'
    return ret
