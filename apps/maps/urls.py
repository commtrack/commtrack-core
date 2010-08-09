from django.conf.urls.defaults import *
import maps.views as views

urlpatterns = patterns('',
    (r'^mapview$', 'maps.views.index'),
)