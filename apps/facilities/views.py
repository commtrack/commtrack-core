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
from hq.models import ReporterProfile

from reporters.utils import *
from reporters.views import message, check_reporter_form, update_reporter
from reporters.models import *

from facilities.models import *
from resources.models import Resource

facilities_set = False


from reporters.utils import *

@login_and_domain_required
def index(req):
    template_name="facilities/index_flat.html"
    columns = (("added_date", "Date Added"),
               ("name", "Name"),
               ("location", "Location"),
               ("description","Description"),
               )
    sort_column, sort_descending = _get_sort_info(req, default_sort_column="added_date",
                                                  default_sort_descending=True)
    sort_desc_string = "-" if sort_descending else ""
    search_string = req.REQUEST.get("q", "")

    query = Facility.objects.order_by("%s%s" % (sort_desc_string, sort_column))

    if search_string == "":
        query = query.all()

    else:
        query = query.filter(
           Q(name__icontains=search_string))
           #Q(location__icontains=search_string))

    facilities = paginated(req, query)
    return render_to_response(req, template_name, {"columns": columns,
                                                   "facilities": facilities,
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

def check_facility_form(req):

    # verify that all non-blank
    # fields were provided
    missing = []
#        field.verbose_name
#        for field in Resource._meta.fields
#        if req.POST.get(field.name, "") == ""
#           and field.blank == False]

    exists = []
    name = req.POST.get("name","")
    if Facility.objects.filter( name=name ):
        exists = ['name']

    # TODO: add other validation checks,
    # or integrate proper django forms
    return {
        "missing": missing,
        "exists": exists }

@require_http_methods(["GET", "POST"])
@login_and_domain_required
def add_facilities(req):

    def get(req):
        template_name = "facilities/index.html"
        facilities = Facility.objects.all().filter(domain=req.user.selected_domain)
        locations = Location.objects.all()

        return render_to_response(req,
                template_name, {
                "facilities": paginated(req, facilities, prefix="facility"),
                "locations": locations,
            })

    @transaction.commit_manually
    def post(req):
        # check the form for errors
        notice_errors = check_facility_form(req)

        # if any fields were missing, abort.
        missing = notice_errors["missing"]
        exists = notice_errors["exists"]

        if missing:
            transaction.rollback()
            return message(req,
                "Missing Field(s): %s" % comma(missing),
                link="/facilities/add")
        # if a resource with the same code is already register abort
        if exists:
            transaction.rollback()
            return message(req,
                "%s already exist" % comma(exists),
                link="/facilities/add")

        try:
            # create the resource object from the form
            facility = Facility()

            loc = Location.objects.get(pk = req.POST.get("location",""))
            facility.location = loc

            latitude = req.POST.get("latitude","")
            if latitude == "":
                latitude = None
            longitude = req.POST.get("longitude","")
            if longitude == "":
                longitude = None

            facility.latitude = latitude
            facility.longitude = longitude
            facility.name = req.POST.get("name","")
            facility.description = req.POST.get("description", "")
            facility.domain = req.user.selected_domain

            # save the changes to the db
            facility.save()
            transaction.commit()

            # full-page notification
            return message(req,
                "A facility %s added" % (facility.pk),
                link="/facilities")

        except Exception, err:
            transaction.rollback()
            raise

    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)

@login_and_domain_required
def edit_facilities(req, pk):
    facility = get_object_or_404(Facility, pk=pk)

    def get(req):
        template_name = "facilities/index.html"
        locations = Location.objects.all()

        return render_to_response(req,
                template_name, {
                "facility":  facility,
                "locations": locations,
            })

    @transaction.commit_manually
    def post(req):
        # delete notification if a delete button was pressed.
        if req.POST.get("delete", ""):
            pk = facility.pk
            facility.delete()

            transaction.commit()
            return message(req,
                "Facility %d deleted" % (pk),
                link="/facilities")
        else:
            # check the form for errors
            notice_errors = check_facility_form(req)

            # if any fields were missing, abort.
            missing = notice_errors["missing"]
            exists = notice_errors["exists"]

            if missing:
                transaction.rollback()
                return message(req,
                    "Missing Field(s): %s" % comma(missing),
                    link="/facilities/add")

            try:
                loc = Location.objects.get(pk = req.POST.get("location",""))
                facility.location = loc

                latitude = req.POST.get("latitude","")
                if latitude == "":
                    latitude = None
                longitude = req.POST.get("longitude","")
                if longitude == "":
                    longitude = None

                facility.latitude = latitude
                facility.longitude = longitude
                facility.name = req.POST.get("name","")
                facility.description = req.POST.get("description", "")
                facility.domain = req.user.selected_domain

                # save the changes to the db
                facility.save()
                transaction.commit()

                # full-page notification
                return message(req,
                    "A facility %s updated" % (facility.pk),
                    link="/facilities")

            except Exception, err:
                transaction.rollback()
                raise

    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)

@login_and_domain_required
def delete_facilities(req, pk):
    facility = get_object_or_404(Facility, pk=pk)
    facility.delete()

    transaction.commit()
    id = int(pk)
    return message(req,
        "A facility %d deleted" % (id),
        link="/facilities")

def confirm(req, pk):
    def get_reporter(current_user, station):
        # todo: get the testers in the system with the same
        # domain as the login user.
        rep_profile = ReporterProfile.objects.filter(domain=current_user.selected_domain)
        rep_profile = rep_profile.filter(facility=station)
        reporters = []
    
        if rep_profile:
            for rep in rep_profile:
                reporter = rep.reporter
                reporters.append(reporter)
        return reporters
    
    def get_resource(station):
        resources = Resource.objects.filter(facility = station)
        return resources

    template_name = 'facilities/confirm.html'
    
    facility = get_object_or_404(Facility, pk=pk)
    if facility:
        personnel = len(get_reporter(req.user, facility))
        resources = get_resource(facility).count()
        
    else:
        return message(req,
        "A facility not found!" % (id),
        link="/facilities")
    
    return render_to_response(req,
                              template_name,
                              {'facility':facility,
                               'personnel':personnel,
                               'resources':resources,
                               }
                              )

def comma(string_or_list):
    """ TODO - this could probably go in some sort of global util file """
    if isinstance(string_or_list, basestring):
        string = string_or_list
        return string
    else:
        list = string_or_list
        return ", ".join(list)

