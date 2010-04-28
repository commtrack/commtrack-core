import datetime

from django.db import models
from django.contrib.auth.models import User

from reporters.models import Reporter
from facilities.models import Facility

#TODO:  Domain in the hp app is much similiar to the
#       the facility in the commtrack. hence a simple verbose
#       name will do the trick, to bring a bit of feeling and
#       slight tweek of the hq.model will be enuf to put the
#       facility and users in place.


#TODO:  Add resources to no specific facility,
#       and then allow them to be allocated,
#       have the quantity of a resource. eg contena of vaccine.

class ResourceCategory(models.Model):
    '''
    This is the division of resources, in groups of similar traits. eg Furniture
    as a general category of all furnitures ie chairs, tables...
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Resource Category'
        verbose_name_plural = 'Resource Categories'

    def __unicode__(self):
        return self.name

class Status(models.Model):
    '''
        The status (or condition) of a resource. eg Good, Normal
    '''
    status = models.CharField(max_length=50)

    def __unicode__(self):
        return self.status


class Resource(models.Model):
    '''
    A resource is an object with........
    '''
    name = models.CharField(max_length=50)
#   A resource can be in only one category this currently works.. but will change to ManyToMany
    category = models.ForeignKey(ResourceCategory, blank=True, null=True)
    code = models.CharField(max_length=256, help_text='unique identifier of the resource')

#   TODO: location shuld be linkin to a facility, create a facility app.
#   a facility shuld be in a domain.
    facility = models.ForeignKey(Facility, blank=True, null=True)
    status = models.ForeignKey(Status)
    description = models.CharField(max_length=256, null=True, blank=True)
    status_change_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class TrackResource(models.Model):
    resource = models.ForeignKey(Resource)
    user = models.ForeignKey(Reporter)
    date_tracked = models.DateTimeField(default=datetime.datetime.now())
    status = models.ForeignKey(Status)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return '%s : %s' % (self.resource, self.date_tracked)

class ResourceSupplyRequest(models.Model):
    user = models.ForeignKey(Reporter)
    resource = models.ForeignKey(Resource)
    request_date = models.DateTimeField(default=datetime.datetime.now())
    request_remarks = models.CharField(max_length=256, null=True, blank=True)
#    user is assign to a domain, and/or facility
#    facility = models.ForeignKey(Facility)

    def __unicode__(self):
        return '%s' % (self.user)
    