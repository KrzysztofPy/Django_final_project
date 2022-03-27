from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    number = models.IntegerField(unique=True)
    login = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


PLACES = (
    (0, "DjangoMED_1"),
    (1, "DjangoMED_2"),
    (2, "DjangoMED_3"),
    (3, "DjangoMED_4")
)


class Place(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)

    def __str__(self):
        return self.name


"""
ROOM_NAMES = (
    (0, "1A"),
    (1, "2A"),
    (2, "3A"),
    (3, "4A"),
    (4, "1B"),
    (5, "2B"),
    (6, "3B"),
    (7, "4B")
)


class Room(models.Model):
    name = models.CharField(max_length=10)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
"""

PHYSICIAN_SPECIALITIES = (
        (0, "---"),
        (1, "Internal medicine"),
        (2, "Pediatrician"),
        (3, "Family medicine"),
        (4, "Dermatologist"),
        (5, "Cardiologist"),
        (6, "Endocrinologist"),
        (7, "Gastroenterologist"),
        (8, "Neurologist"),
        (9, "Urologist"),
        (10, "Radiologist"),
        (11, "Orthopaedist")
    )


class PhysicianSpeciality(models.Model):
    speciality = models.IntegerField(choices=PHYSICIAN_SPECIALITIES)
    description = models.TextField()

    def __str__(self):
        return PHYSICIAN_SPECIALITIES[self.speciality][1]


RATE = (
    (0, "*"),
    (1, "**"),
    (2, "***"),
    (3, "****"),
    (4, "*****")
)


class Doctor(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    rating = models.IntegerField(choices=RATE, null=True, blank=True)
    speciality = models.ManyToManyField(PhysicianSpeciality)
    places = models.ManyToManyField(Place)

    def __str__(self):
        return f"Doctor {self.name[0]} {self.surname}"


"""
class Notification(models.Model):
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    place = models.ManyToManyField(Place)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_date} visit with {self.doctor}"
"""


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=24, default='0:20 minutes')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.date} at {self.time}"

