from django import forms
import datetime
from appointment_app.models import Appointment

#Needed for user login and authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


#form to user logging in
class LoginForm(AuthenticationForm):
    class Meta:
        model = User

HOURS = (
    (0, "08"),
    (1, "09"),
    (2, "10"),
    (3, "11"),
    (4, "12")
)
MINUTES = (
    (0, '00'),
    (1, '20'),
    (2, '40')
)

#form to add new appointment
class AppAddForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    time_hour = forms.ChoiceField(choices=HOURS)
    time_minute = forms.ChoiceField(choices=MINUTES)
    #duration = forms.CharField(max_length=24)
    # place = forms.ForeignKey(Place, on_delete=models.CASCADE)
    # doctor = forms.ForeignKey(Doctor, on_delete=models.CASCADE)


#form to search for free appointments for given date
class AppSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    date_to = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)

