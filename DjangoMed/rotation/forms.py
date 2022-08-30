from django import forms
import datetime


from appointment_app.forms import ALL_PLACES


class RotationSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    date_to = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    place = forms.ChoiceField(choices=ALL_PLACES)


