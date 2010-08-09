from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap

from hq.models import *

from reporters.models import Reporter
from locations.models import Location

from facilities.models import *

GMAP = GoogleMap(key='ABQIAAAAwLx05eiFcJGGICFj_Nm3yxSy7OMGWhZNIeCBzFBsFwAAIleLbBRLVT87XVW-AJJ4ZR3UOs3-8BnQ-A') # Can also set GOOGLE_MAPS_API_KEY in settings

class FacilityAdmin(admin.OSMGeoAdmin):
    search_fields = ('name','code')
    list_display = ('name','location','domain','added_date')
    list_filter = ('domain',)

admin.site.register(Facility, FacilityAdmin)

