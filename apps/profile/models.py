from django.db import models

from locations.models import Location

class OrgProfile(models.Model):
    """
        Profile for organazations using the system.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    address = models.TextField()
    country = models.ForeignKey(Location)
