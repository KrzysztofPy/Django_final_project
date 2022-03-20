from django import forms

from appointment_app.models import Appointment

#Needed for user login and authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


#form to user logging in
class LoginForm(AuthenticationForm):
    class Meta:
        model = User


#for to search for free appointments for given date
class AppSearchForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)

