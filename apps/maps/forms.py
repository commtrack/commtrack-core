from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from resources.models import Status

class FilterChoiceForm(forms.Form):
    '''
        filtering maps data(marker) to certain required data.
    '''
    start_date = forms.DateField(widget = widgets.AdminDateWidget())
    end_date = forms.DateField(widget = widgets.AdminDateWidget())
    resource_status = forms.ModelMultipleChoiceField(queryset=Status.objects.all())
    