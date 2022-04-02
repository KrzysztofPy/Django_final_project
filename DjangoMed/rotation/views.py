from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    PermissionDenied
)

from django.db import IntegrityError


from rotation.models import Rotation
from appointment_app.models import Appointment, Patient


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        rotation_appts = Rotation.objects.filter(user1=request.user.pk)
        rotation_appts_list = []
        for rappts in rotation_appts:
            rotation_appts_list.append(rappts.appointment_2rotate_id)
        booked_appts = Appointment.objects.filter(user=request.user.pk).exclude(pk__in=rotation_appts_list)

        return render(request, "rotation/list_appts_2rotate.html", {"bappts": booked_appts,
                                                                    "rappts": rotation_appts
                                                                    })

    def post(self, request):
        # mapping buttons values to variables. Pressed button will change value from None to swap_me or demote_me
        swap_visit_yes = request.POST.get('swap') #if button pressed then value is 'swap_me_{{ appointment.id }}'
        demote_visit_yes = request.POST.get('demote') #if button pressed then value is 'demote_me_{{ rotation.appointment_2rotate.pk }}'
        #print(swap_visit_yes)
        if swap_visit_yes:
            try:
                booked_appt_2swap = Appointment.objects.get(id=int(swap_visit_yes[8:]))
                #print(f"booked_appt_2swap.pk={booked_appt_2swap.pk}")
                #print(f"booked_appt_2swap.id={booked_appt_2swap.id}")
                #print(f"request.user.pk= {request.user.pk}")
                # creates the row in the Rotation table with the Appointment.pk and the user1 as currently loggedin user
                Rotation.objects.create(appointment_2rotate_id=booked_appt_2swap.id, user1=Patient.objects.get(user_id=request.user.pk))
                return redirect('rotation:home')
            except IntegrityError:
                messages.warning(request, "Only one appointment on SWAP allowed!")
                return redirect('rotation:home')
        if demote_visit_yes:
            Rotation.objects.get(appointment_2rotate_id=int(demote_visit_yes[10:])).delete() # deletes the whole row in the Rotation table
            return redirect('rotation:home')
        #print(booked_appt_2swap)
        #form = RotationSearchForm(request.POST)
        #if form.is_valid():

        return HttpResponse("ups")
