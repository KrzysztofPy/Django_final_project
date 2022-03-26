from django import forms
import datetime
from appointment_app.models import Appointment


#Imports from the models
from appointment_app.models import PHYSICIAN_SPECIALITIES, Doctor, Place


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


def get_places(places_model):
    all_places = places_model.objects.all()
    ALL_PLACES = [(0, "---")]
    for place in all_places:
        ALL_PLACES.append((place.pk, place.name))
    return tuple(ALL_PLACES)


def get_doctors(doctors_model):
    all_doctors = doctors_model.objects.all()
    ALL_DOCTORS = [(0, "---")]
    for doctor in all_doctors:
        ALL_DOCTORS.append((doctor.pk, doctor.name))
    return tuple(ALL_DOCTORS)


#form to add new appointment
class AppAddForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    time_hour = forms.ChoiceField(choices=HOURS)
    time_minute = forms.ChoiceField(choices=MINUTES)
    #duration = forms.CharField()
    #place = forms.ForeignKey(Place)
    #doctor = forms.ForeignKey(Doctor)


#form to search for free appointments for given date
class AppSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    date_to = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    doctor_speciality = forms.ChoiceField(choices=PHYSICIAN_SPECIALITIES)
    place = forms.ChoiceField(choices=get_places(Place))

