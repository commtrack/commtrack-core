from django.conf.urls.defaults import *
import maps.views as views

urlpatterns = patterns('',
    (r'^mapview$', 'maps.views.index'),
    (r'^map/resource/(?P<pk>\d+)$', 'maps.views.map_resource'),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
)