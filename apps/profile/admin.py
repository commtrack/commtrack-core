from django.contrib import admin

from profile.models import OrgProfile


from facilities.models import *

#class OrgProfileAdmin(admin.ModelAdmin):
#    search_fields = ('name',)
#    list_display = ('name')
#admin.site.register(OrgProfile, OrgProfileAdmin)
admin.site.register(OrgProfile)

