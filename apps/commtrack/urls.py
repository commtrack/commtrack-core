from django.conf.urls.defaults import *
import commtrack.views as views

urlpatterns = patterns('',
    (r'^testers$', 'commtrack.views.index'),
    (r'^testers/add$', 'commtrack.views.add_testers'),
    (r'^testers/(?P<pk>\d+)$', 'commtrack.views.edit_testers'),
    (r'^testers/(?P<pk>\d+)/delete$', 'commtrack.views.delete_testers'),
)