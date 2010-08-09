import datetime

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

@login_and_domain_required
def index(req):
    facilities = Facility.objects.all().order_by('name')
    
    return render_to_response(req, 
                              'mapindex.html',
                              {'facilities': facilities},                              
                              )


@login_and_domain_required
def facilities(req):
    facilities = Facility.objects.all().order_by('name')
        
    return render_to_response(req,'mapindex.html', {
        'facilities': facilities,
        'content': render_to_string('facilities.html', {'facilities' : facilities}),
    })