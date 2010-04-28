from datetime import datetime

from django.db import models

from domain.models import Domain
from locations.models  import Location

#   TODO:   Think how the parent location of the facility
#           will be potrayed.. in a model.

class Facility(models.Model):
    name = models.CharField(max_length=65)
    domain = models.ForeignKey(Domain)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, help_text='the geographical location where this facility is, eg city, town')
    added_date = models.DateTimeField(default = datetime.now())

    # Point co-ordinates of a facility
    latitude  = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, help_text="The physical latitude of this location")
    longitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, help_text="The physical longitude of this location")

    class Meta:
        verbose_name_plural = 'Facilities'

    def __unicode__(self):
        return self.name

# RE-think
#class Address(models.Model):
#    address = models.TextField()
