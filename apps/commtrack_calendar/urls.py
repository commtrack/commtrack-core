from django.conf.urls.defaults import *

## calendar view
urlpatterns = patterns('commtrack_calendar.views',
    (r'^calender$', 'view'),
    (r'^samplepop/$', 'samples_pop'),

)


