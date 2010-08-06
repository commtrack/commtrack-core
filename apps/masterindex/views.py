import resource
import logging
import hashlib
import settings
import traceback
import sys
import os
import uuid
import string
from datetime import timedelta
from graphing import dbhelper

from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.exceptions import *
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rapidsms.webui.utils import render_to_response, paginated

from domain.decorators import login_and_domain_required
from xformmanager.models import *
from hq.models import *
from graphing.models import *
from receiver.models import *

import hq.utils as utils
import hq.reporter as reporter
import hq.reporter.custom as custom
import hq.reporter.metastats as metastats

import hq.reporter.inspector as repinspector
import hq.reporter.metadata as metadata

from reporters.utils import *
from reporters.views import message, check_reporter_form, update_reporter
from reporters.models import *

from resources.models import *
from masterindex.models import MasterIndex

resources_set = False


from reporters.utils import *

def index(req):
    template_name = 'masterindex.html'
    columns = (("resource", "Resource"),
               ("facility", "Facility"),
               )
    sort_column, sort_descending = _get_sort_info(req, default_sort_column="resource",
                                                  default_sort_descending=True)
    sort_desc_string = "-" if sort_descending else ""
    search_string = req.REQUEST.get("q", "")

    query = MasterIndex.objects.order_by("%s%s" % (sort_desc_string, sort_column))

    if search_string == "":
        query = query.all()

    else:
        query = query.filter(
           Q(resource__name__icontains=search_string) |
           Q(facility__name__icontains=search_string))

    indexies = paginated(req, query)
    return render_to_response(req, template_name, {"columns": columns,
                                                   "indexies": indexies,
                                                   "sort_column": sort_column,
                                                   "sort_descending": sort_descending,
                                                   "search_string": search_string})

def _get_sort_info(request, default_sort_column, default_sort_descending):
    sort_column = default_sort_column
    sort_descending = default_sort_descending
    if "sort_column" in request.GET:
        sort_column = request.GET["sort_column"]
    if "sort_descending" in request.GET:
        if request.GET["sort_descending"].startswith("f"):
            sort_descending = False
        else:
            sort_descending = True
    return (sort_column, sort_descending)
