from django import forms
from django.forms import ModelForm

FILTER_CHOICES = (
                    ('all', 'All'),
                    ('res', 'Resources'),
                    ('faci', 'Facilities'),
                  )

class FilterChoiceForm(forms.Form):
    '''
        filtering maps data(marker) to certain required data.
    '''
    filter = forms.CharField(max_length=4, widget=forms.Select(choices=FILTER_CHOICES))