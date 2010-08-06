from django.conf.urls.defaults import *
import masterindex.views as views

urlpatterns = patterns('',
    (r'^masterindex$', 'masterindex.views.index'),
)