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

resources_set = False


from reporters.utils import *


#def get_tester(current_user):
#    # todo: get the testers in the system with the same
#    # domain as the login user.
#    rep_profile = ReporterProfile.objects.filter(domain=current_user.selected_domain)
#    reporters = []
#
#    if rep_profile:
#        for rep in rep_profile:
#            reporter = rep.reporter
#            reporters.append(reporter)
#    return reporters

#@login_and_domain_required
#def index(req):
#    resources = Resource.objects.all()
#    return render_to_response(req,
#        "resources/index.html", {
#        # "resources": paginated(req, resources, prefix="res"),
#        "resources": resources,
#    })

@login_and_domain_required
def index(req):
    template_name="resources/index_flat.html"
    columns = (("date_added", "Date Added"),
               ("name", "Name"),
               ("code", "Code"),
               ("facility", "Facility"),
               ("status", "Status"))
    sort_column, sort_descending = _get_sort_info(req, default_sort_column="date_added",
                                                  default_sort_descending=True)
    sort_desc_string = "-" if sort_descending else ""
    search_string = req.REQUEST.get("q", "")

    query = Resource.objects.order_by("%s%s" % (sort_desc_string, sort_column))

    if search_string == "":
        query = query.all()

    else:
        query = query.filter(
           Q(code__icontains=search_string) |
           Q(name__icontains=search_string))

    resources = paginated(req, query)
    return render_to_response(req, template_name, {"columns": columns,
                                                   "resources": resources,
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

def check_resource_form(req):

    # verify that all non-blank
    # fields were provided
    missing = []
#        field.verbose_name
#        for field in Resource._meta.fields
#        if req.POST.get(field.name, "") == ""
#           and field.blank == False]

    exists = []
    code = req.POST.get("code","")
    if Resource.objects.filter( code=code ):
        exists = ['code']

    # TODO: add other validation checks,
    # or integrate proper django forms
    return {
        "missing": missing,
        "exists": exists }

@require_http_methods(["GET", "POST"])
@login_and_domain_required
def add_resources(req):

    def get(req):
        template_name = "resources/index.html"
        resources = Resource.objects.all()
        categories = ResourceCategory.objects.all()
        facilities = Facility.objects.all().filter(domain=req.user.selected_domain)
        status = Status.objects.all()
        
        return render_to_response(req,
                template_name, {
                "resources": paginated(req, resources, prefix="resource"),
                "categories" : categories,
                "facilities" : facilities,
                "status" : status,
            })

    @transaction.commit_manually
    def post(req):
        # check the form for errors
        notice_errors = check_resource_form(req)

        # if any fields were missing, abort.
        missing = notice_errors["missing"]
        exists = notice_errors["exists"]

        if missing:
            transaction.rollback()
            return message(req,
                "Missing Field(s): %s" % comma(missing),
                link="/resources/add")
        # if a resource with the same code is already register abort
        if exists:
            transaction.rollback()
            return message(req,
                "%s already exist" % comma(exists),
                link="/resources/add")

        #TODO: Finish adding a resource.
        try:
            # create the resource object from the form
            resource = Resource()

            cat = ResourceCategory.objects.get(pk = req.POST.get("category",""))
            resource.category = cat

            status = Status.objects.get(pk = req.POST.get("status",""))
            resource.status = status

            facility = Facility.objects.get(pk = req.POST.get("facility",""))
            resource.facility = facility
            
            resource.name = req.POST.get("name","")
            resource.code = req.POST.get("code","")


            # save the changes to the db
            resource.save()
            transaction.commit()

            # full-page notification
            return message(req,
                "A resource %s added" % (resource.pk),
                link="/resources")

        except Exception, err:
            transaction.rollback()
            raise

    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)

@login_and_domain_required
def edit_resources(req, pk):
    resource = get_object_or_404(Resource, pk=pk)

    def get(req):
        template_name = "resources/index.html"
        resources = Resource.objects.all()
        categories = ResourceCategory.objects.all()
        facilities = Facility.objects.all().filter(domain=req.user.selected_domain)
        status = Status.objects.all()

        return render_to_response(req,
                template_name, {
                "resources": paginated(req, resources, prefix="resource"),
                "categories" : categories,
                "facilities" : facilities,
                "status" : status,
                "resource" : resource,
            })
            
    @transaction.commit_manually
    def post(req):
        # delete notification if a delete button was pressed.
        if req.POST.get("delete", ""):
            pk = resource.pk
            resource.delete()

            transaction.commit()
            return message(req,
                "Resource %d deleted" % (pk),
                link="/resources")
        else:
            # check the form for errors
            notice_errors = check_resource_form(req)

            # if any fields were missing, abort.
            missing = notice_errors["missing"]
            exists = notice_errors["exists"]

            if missing:
                transaction.rollback()
                return message(req,
                    "Missing Field(s): %s" % comma(missing),
                    link="/resources/add")

            try:
                # create the resource object from the form
                cat = ResourceCategory.objects.get(pk = req.POST.get("category",""))
                resource.category = cat

                status = Status.objects.get(pk = req.POST.get("status",""))
                resource.status = status
                
                pk = req.POST.get("facility","")
                if pk != "":
                    facility = Facility.objects.get(pk = req.POST.get("facility",""))
                    resource.facility = facility
                else:
                    resource.facility = None

                resource.name = req.POST.get("name","")
                resource.code = req.POST.get("code","")


                # save the changes to the db
                resource.save()
                transaction.commit()

                # full-page notification
                return message(req,
                    "A resource %s updated" % (resource.pk),
                    link="/resources")

            except Exception, err:
                transaction.rollback()
                raise

    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)

@login_and_domain_required
def delete_resources(req, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.delete()

    transaction.commit()
    id = int(pk)
    return message(req,
        "A resource %d deleted" % (id),
        link="/resources")

def comma(string_or_list):
    """ TODO - this could probably go in some sort of global util file """
    if isinstance(string_or_list, basestring):
        string = string_or_list
        return string
    else:
        list = string_or_list
        return ", ".join(list)

def resource_requests(req):
    """
        display resource supply requests from the user within the domain.
    """
#    resource_req = ResourceSupplyRequest.objects.all()
    template_name="resources/requests.html"

    columns = (("request_date", "Date Of Request"),
               ("user", "Requester"),
               ("resource", "Resource"),
               ("request_remarks", "Remarks"),
               ("status", "Status"))
    sort_column, sort_descending = _get_sort_info(req, default_sort_column="request_date",
                                                  default_sort_descending=True)
    sort_desc_string = "-" if sort_descending else ""
    search_string = req.REQUEST.get("q", "")

    query = ResourceSupplyRequest.objects.order_by("%s%s" % (sort_desc_string, sort_column))

    if search_string == "":
        query = query.all()

    else:
        query = query.filter(
           Q(status__icontains=search_string)|
           Q(user__first_name__icontains=search_string)|
           Q(resource__name__icontains=search_string)|
           Q(resource__code__icontains=search_string)|
           Q(user__last_name__icontains=search_string))

    resource_reqs = paginated(req, query)
    return render_to_response(req, template_name, {"columns": columns,
                                                   "resource_reqs": resource_reqs,
                                                   "sort_column": sort_column,
                                                   "sort_descending": sort_descending,
                                                   "search_string": search_string})

@login_and_domain_required
def accept_resource_requests(req, pk):
    resource_req = get_object_or_404(ResourceSupplyRequest, pk=pk)
    resource_req.status = 'Accepted'
    resource_req.save()

#    transaction.commit()
    id = int(pk)
    return message(req,
        "A resource request %d is Accepted" % (id),
        link="/resources/requests")

@login_and_domain_required
def deny_resource_requests(req, pk):
    resource_req = get_object_or_404(ResourceSupplyRequest, pk=pk)
    resource_req.status = 'Denied'
    resource_req.save()

#    transaction.commit()
    id = int(pk)
    return message(req,
        "A resource request %d is Denied" % (id),
        link="/resources/requests")

def resource_history(req):
    """
        display resources' history
    """
    template_name="resources/history.html"

    columns = (("date", "Date Of Request"),
               ("name", "Name"),
               ("code", "Code"),
               ("Facility", "Current Location"))
#               ("New", "Prev Location")) #previous location  
    sort_column, sort_descending = _get_sort_info(req, default_sort_column="date",
                                                  default_sort_descending=True)
    sort_desc_string = "-" if sort_descending else ""
    search_string = req.REQUEST.get("q", "")

    query = Resource.objects.order_by("%s%s" % (sort_desc_string, sort_column))

    if search_string == "":
        query = query.all()

    else:
        query = query.filter(
           Q(status__icontains=search_string)|
           Q(user__first_name__icontains=search_string))

    history = paginated(req, query)
    return render_to_response(req, template_name, {"columns": columns,
                                                   "history": history,
                                                   "sort_column": sort_column,
                                                   "sort_descending": sort_descending,
                                                   "search_string": search_string})