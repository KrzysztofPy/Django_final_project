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
    """This function gets the Place model and creates a tuple of tuples ((0, '---'), (1, 'place.name'), ...)"""
    all_places = places_model.objects.all()
    ALL_PLACES = [(0, "---")]
    for place in all_places:
        ALL_PLACES.append((place.pk, place.name))
    return tuple(ALL_PLACES)


ALL_PLACES = get_places(Place)


def get_doctors(doctors_model):
    all_doctors = doctors_model.objects.all()
    ALL_DOCTORS = [(0, "---")]
    for doctor in all_doctors:
        temp = [doctor.name, doctor.surname]
        ALL_DOCTORS.append((doctor.pk, " ".join(temp)))
    return tuple(ALL_DOCTORS)


ALL_DOCTORS = get_doctors(Doctor)


def get_doctors_specialities(doctors_model):
    all_specialities = doctors_model.objects.all()
    ALL_DOCTORS_SPECIALITIES = [(0, "---")]
    for speciality in all_specialities:
        ALL_DOCTORS_SPECIALITIES.append((speciality.pk, speciality.speciality))
    return tuple(ALL_DOCTORS_SPECIALITIES)


ALL_DOCTORS_SPECIALITIES = get_doctors_specialities(Doctor)


#form to add new appointment
class AppAddForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    time_hour = forms.ChoiceField(choices=HOURS)
    time_minute = forms.ChoiceField(choices=MINUTES)
    #duration = forms.CharField()
    place = forms.ChoiceField(choices=ALL_PLACES)
    doctor = forms.ChoiceField(choices=ALL_DOCTORS)
    speciality = forms.ChoiceField(choices=ALL_DOCTORS_SPECIALITIES)


#form to search for free appointments for given date
class AppSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    date_to = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    doctor_speciality = forms.ChoiceField(choices=PHYSICIAN_SPECIALITIES)
    place = forms.ChoiceField(choices=ALL_PLACES)

