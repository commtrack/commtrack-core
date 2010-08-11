from django import forms
from django.forms import ModelForm
from sms_notifications.models import SmsNotification

class SmsNotificationForm(ModelForm):
    class Meta:
        model = SmsNotification
        exclude = ('modified','created','domain')