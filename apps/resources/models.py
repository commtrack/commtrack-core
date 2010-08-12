import datetime

from django.db import models
from django.contrib.auth.models import User

from reporters.models import Reporter
from facilities.models import Facility

#import audit

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
    
    def __str__(self):
        return "%s" % (self.name,)

class Status(models.Model):
    '''
        The status (or condition) of a resource. eg Good, Normal
    '''
    status = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'status'
    
    def __str__(self):
        return self.status
    
    def __unicode__(self):
        return self.status


class Resource(models.Model):
    '''
    A resource is an object
    '''
    name = models.CharField(max_length=50)
#   A resource can be in only one category this currently works.. but will change to ManyToMany
    category = models.ForeignKey(ResourceCategory, blank=True, null=True)
    code = models.CharField(max_length=256, help_text='unique identifier of the resource')
    facility = models.ForeignKey(Facility, blank=True, null=True)
    status = models.ForeignKey(Status)
    description = models.CharField(max_length=256, null=True, blank=True)
    status_change_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
class TrackResource(models.Model):
    resource = models.ForeignKey(Resource)
    user = models.ForeignKey(Reporter)
    date_tracked = models.DateTimeField(default=datetime.datetime.now())
    status = models.ForeignKey(Status)
    description = models.CharField(max_length=256, null=True, blank=True)
    
    def __unicode__(self):
        return '%s : %s' % (self.resource, self.date_tracked)

    def __str__(self):
        return '%s tracked %s' % (self.resource.name, self.date_tracked)
    
class ResourceSupplyRequest(models.Model):
    REQUEST_STATUS_CHOICES= (
            ('pending','Pending'),
            ('accepted','Accepted'),
            ('denied','Denied'),
    )
    user = models.ForeignKey(Reporter)
    resource = models.ForeignKey(Resource)
    request_date = models.DateTimeField(default=datetime.datetime.now())
    request_remarks = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default=REQUEST_STATUS_CHOICES[0])
        
    def __unicode__(self):
        return '%s' % (self.user)

    def __str__(self):
        return '%s requested by %s' % (self.resource.name, self.user)