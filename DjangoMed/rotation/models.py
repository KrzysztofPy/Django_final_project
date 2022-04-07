from django.db import models
from django.contrib.auth.models import User

from appointment_app.models import Appointment, Patient


class Rotation(models.Model):
    appointment_2rotate = models.OneToOneField(Appointment, on_delete=models.CASCADE, blank=True, null=True)
    user1 = models.OneToOneField(Patient, related_name="user1", on_delete=models.CASCADE, blank=True, null=True)
    user2 = models.OneToOneField(Patient, related_name="user2", on_delete=models.CASCADE, blank=True, null=True)
    user1_agree = models.BooleanField(default=False)

    def __str__(self):
        return f"Rotation visit: {self.appointment_2rotate}"
