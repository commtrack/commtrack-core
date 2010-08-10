from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.fields import CharField
from resources.models import Status

FILTER_CHOICES = (
                    ('res', 'Resources'),
                    ('faci', 'Facilities'),
                  )

class FilterChoiceForm(forms.Form):
    '''
        filtering maps data(marker) to certain required data.
    '''
    filter_type = forms.CharField(max_length=4,widget=forms.Select(choices=FILTER_CHOICES))
    start_date = forms.DateField(widget = widgets.AdminDateWidget())
    end_date = forms.DateField(widget = widgets.AdminDateWidget())
    resource_status = forms.ModelMultipleChoiceField(queryset=Status.objects.all())
    