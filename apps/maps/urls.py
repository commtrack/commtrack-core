from django.conf.urls.defaults import *
import maps.views as views

urlpatterns = patterns('',
    (r'^mapview$', 'maps.views.index'),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
)