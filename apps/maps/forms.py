from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.fields import CharField
from resources.models import Status

FILTER_CHOICES = (
                    ('all', 'All'),
                    ('res', 'Resources'),
                    ('faci', 'Facilities'),
                  )

class FilterChoiceForm(forms.Form):
    '''
        filtering maps data(marker) to certain required data.
    '''
    start_date = forms.DateField(widget = widgets.AdminDateWidget())
    end_date = forms.DateField(widget = widgets.AdminDateWidget())
    filter_status = forms.ModelMultipleChoiceField(queryset=Status.objects.all())
    filter_type = forms.SelectMultiple(choices=FILTER_CHOICES)
    