import httplib, urllib
from threading import Thread

from django.db import models
from django.db.models.signals import post_save

from resources.models import Resource
from facilities.models import Facility
from domain.models import Domain


class MasterIndex(models.Model):
    resource = models.ForeignKey(Resource)
    facility = models.ForeignKey(Facility, null=True, blank=True)
    
    # to keep master index separate within domains.
    domain = models.ForeignKey(Domain)
    
    class Meta:
        verbose_name_plural = 'Master Indexies'
        
    def __unicode__(self):
        return '%s is now at %s' % (self.resource, self.facility)
    
    def save(self, **kwargs):
        # modifed save to replace or add new resource allocations
        # add a filter for domain.
        MasterIndex.objects.filter(resource=self.resource).delete()
        super(MasterIndex, self).save(**kwargs)

def update_masterindex(sender, instance, created, **kwargs):
    MasterIndex(resource = instance,
                facility = instance.facility,
                domain = instance.facility.domain,
                ).save()
        
# signal to trigger masterindex update each time a Resource is saved
post_save.connect(update_masterindex, sender=Resource)