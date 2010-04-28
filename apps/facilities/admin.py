from django.contrib import admin
from django.contrib.auth.models import Group, User

from hq.models import *

from reporters.models import Reporter
from locations.models import Location

from facilities.models import *

class FacilityAdmin(admin.ModelAdmin):
    search_fields = ('name','code')
    list_display = ('name','location','domain','added_date')
    list_filter = ('domain',)

admin.site.register(Facility, FacilityAdmin)

