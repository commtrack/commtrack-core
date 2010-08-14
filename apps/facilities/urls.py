from django.conf.urls.defaults import *
import facilities.views as views

urlpatterns = patterns('',
    (r'^facilities$', 'facilities.views.index'),
    (r'^facilities/add$', 'facilities.views.add_facilities'),
    (r'^facilities/(?P<pk>\d+)$', 'facilities.views.edit_facilities'),
    (r'^facilities/(?P<pk>\d+)/delete$', 'facilities.views.confirm'),
    (r'^facilities/(?P<pk>\d+)/delete/confirmed$', 'facilities.views.delete_facilities'),
)