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
@login_and_domain_required
def index(req):
    facilities = Facility.objects.all().order_by('name')
    if req.method == 'POST': # If the form has been submitted...
        form = FilterChoiceForm(req.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # saving the form data is not cleaned
            form.save()
            return HttpResponse('You just submit a form..Horray!')
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
def facilities(req):
    facilities = Facility.objects.all().order_by('name')
        
    return render_to_response(req,'mapindex.html', {
        'facilities': facilities,
        'content': render_to_string('facilities.html', {'facilities' : facilities}),
    })