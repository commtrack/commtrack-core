from datetime import datetime

#from django.db import models
from django.contrib.gis.db import models
from domain.models import Domain
from locations.models  import Location

#import audit
#   TODO:   Think how the parent location of the facility
#           will be potrayed.. in a model.

class Facility(models.Model):
    name = models.CharField(max_length=65)
    domain = models.ForeignKey(Domain)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, help_text='the geographical location where this facility is, eg city, town')
    added_date = models.DateTimeField(default = datetime.now())
    # history = audit.AuditTrail()
    # geodjango - point for the facility location.
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'Facilities'

    def __unicode__(self):
        return self.name

# RE-think
#class Address(models.Model):
#    address = models.TextField()
