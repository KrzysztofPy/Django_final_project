from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from appointment_app.models import Patient, Appointment, Doctor, Place, PhysicianSpeciality #Room


#register models
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(PhysicianSpeciality)
admin.site.register(Place)
#admin.site.register(Room)


# Define an inline admin descriptor for Patient model
# which acts a bit like a singleton
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'patient'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PatientInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
