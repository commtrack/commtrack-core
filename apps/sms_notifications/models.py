from datetime import datetime

from django.db import models

from domain.models import Domain 
from xformmanager.models import FormDefModel
from resources.models import Status
from facilities.models import Facility
from reporters.models import Reporter

class NotificationChoice(models.Model):
    '''
       The xForm to bind with the sms_notification table. 
    '''
    choice = models.CharField(max_length=255)
    xform = models.ForeignKey(FormDefModel)

    def __unicode__(self):
        return self.choice
    
class SmsNotification(models.Model):
    '''
        SMS alerts to the responsible personnel on status change 
        of resource(s).
    '''
    Facility = models.ManyToManyField(Facility, help_text="Hold down Ctrl for multiple selections")
    authorised_personnel = models.ForeignKey(Reporter)
    notification_type = models.ForeignKey(NotificationChoice)
    notification_status = models.ManyToManyField(Status)
    digest = models.BooleanField(default=False)
    modified = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.now)
    domain = models.ForeignKey(Domain, null=True, blank=True)
    
    def __unicode__(self):
            return '%s notification for %s'%(self.notification_type, self.authorised_sampler)
