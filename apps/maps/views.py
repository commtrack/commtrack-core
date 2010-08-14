import datetime
#import simplejson as json
from django.utils import simplejson as json


from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import *

from domain.decorators import login_and_domain_required
from rapidsms.webui.utils import render_to_response, paginated
from facilities.models import Facility
from maps.utils import encode_myway
from maps.forms import FilterChoiceForm
from resources.models import Resource

@login_and_domain_required
def index(req):
    facilities = Facility.objects.all().order_by('name')
    if req.method == 'POST': # If the form has been submitted...
        form = FilterChoiceForm(req.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # saving the form data is not cleaned
            #form.save()
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['resource_status']
            
            resources = Resource.objects.filter(facility__in = facilities)
            resources = resources.filter(status__in = status)
            
            facilities = []
            for resource in resources:
                facilities.append(resource.facility)
            
            print 'START: %s -------------- END: %s ---------- STATUS: %s' % (start_date, end_date, status)
            #return HttpResponse('You just submit a form..Horray!')
    else:
        form = FilterChoiceForm() # An unbound form

    return render_to_response(req, 
                              'mapindex.html',
                              {
                               'facilities': facilities,
                               'form': form,
                               },                              
                              )

@login_and_domain_required
def map_resource(req,pk):
    resource = get_object_or_404(Resource, pk=pk)
    if resource:
        # get a coordinate for the resource
        # currently depends on the assigned facility
        # TODO: allow resource to have independent coordinates 
        point = resource.facility   
    return render_to_response(req,
                              'generic_map.html', 
                              {
                               'point': point,
                               'resource': resource,
                               }
                              )