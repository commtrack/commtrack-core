import httplib, urllib
from threading import Thread

from django.db.models.signals import post_save
from resource.models import Resource
from masterindex.models import MasterIndex
from facilities.models import Facility

# signals failed to work when placed here.. hence moved to model.py

#def update_masterindex(sender, instance, created, **kwargs):
#    print 'here--------------------->>>>'
#    
#    MasterIndex(resource = instance,
#                facility = instance.facility,
#                domain = instance.facility.domain,
#                ).save()
#    
## signal to trigger masterindex update each time a Resource is saved
#post_save.connect(update_masterindex, sender=Resource)