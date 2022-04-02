from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    number = models.IntegerField(unique=True)
    login = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

"""
ROOM_NAMES = (
    (0, "---"),
    (1, "1A"),
    (2, "2A"),
    (3, "3A"),
    (4, "4A"),
    (5, "1B"),
    (6, "2B"),
    (7, "3B"),
    (8, "4B")
)


class Room(models.Model):
    room_name = models.IntegerField(choices=ROOM_NAMES)

    def __str__(self):
        return ROOM_NAMES[self.room_name][1]
"""

PLACES = (
    (0, "DjangoMED_1"),
    (1, "DjangoMED_2"),
    (2, "DjangoMED_3"),
    (3, "DjangoMED_4")
)


class Place(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    #room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    specialities = models.IntegerField(choices=PHYSICIAN_SPECIALITIES)
    description = models.TextField()

    def __str__(self):
        return PHYSICIAN_SPECIALITIES[self.specialities][1]


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

    @property
    def get_rating(self):
        if self.rating:
            return str(RATE[self.rating][1])
        else:
            return f"No rating yet"

    def __str__(self):
        return f"Doc. {self.name[0]} {self.surname}"


"""

"""


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=24, default='0:20 minutes')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    #room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.date} at {self.time}"




"""
class Notification(models.Model):
    visit_date = models.DateTimeField
    visit_date = models.DateTimeField
    place = models.ManyToManyField(Place)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_date} visit with {self.doctor}"
"""
