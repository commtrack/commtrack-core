from django.conf.urls.defaults import *
import sms_notifications.views as views

urlpatterns = patterns('',
    (r'^smsnotification$', 'sms_notifications.views.index'),
    (r'^smsnotification/add$', 'sms_notifications.views.add_notifications'),
    (r'^smsnotification/(?P<pk>\d+)$', 'sms_notifications.views.edit_notifications'),
    (r'^smsnotification/(?P<pk>\d+)/delete$', 'sms_notifications.views.delete_notifications'),
)