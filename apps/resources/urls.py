from django.conf.urls.defaults import *
import resources.views as views

urlpatterns = patterns('',
    (r'^resources$', 'resources.views.index'),
    (r'^resources/add$', 'resources.views.add_resources'),
    (r'^resources/(?P<pk>\d+)$', 'resources.views.edit_resources'),
    (r'^resources/(?P<pk>\d+)/delete$', 'resources.views.delete_resources'),
)