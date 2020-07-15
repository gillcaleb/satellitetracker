from django import forms
from django.core.validators import validate_email


class configForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=128)
    constellation = forms.CharField()
    view = forms.BooleanField(label="Entire Constellation?")
    lat = forms.FloatField(label="Latitude", min_value = -90.0, max_value=90.0)
    long = forms.FloatField(label= "Longitude", min_value = -180.0, max_value=180.0)
    refresh = forms.IntegerField(label="Refresh Rate", min_value = 1)
    filename = forms.CharField(label='File name', max_length=128)
