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
from appointment_app.models import Appointment, Patient, Doctor, PHYSICIAN_SPECIALITIES, Place, PhysicianSpeciality

from appointment_app.forms import ALL_PLACES
from rotation.forms import RotationSearchForm


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        rotation_appts = Rotation.objects.filter(user1=request.user.pk)
        rotation_appts_list = []
        for rappts in rotation_appts:
            rotation_appts_list.append(rappts.appointment_2rotate_id)
        booked_appts = Appointment.objects.filter(user=request.user.pk).exclude(pk__in=rotation_appts_list).order_by('date')

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


class RotationSearchView(View):
    def get(self, request, appointment_2rotate_id):
        appt_2rotate = Appointment.objects.get(pk=appointment_2rotate_id)
        form = RotationSearchForm()
        return render(request, "rotation/rotation_search.html", {"appt_2rotate": appt_2rotate,
                                                                 "form": form})

    def post(self, request, appointment_2rotate_id):
        form = RotationSearchForm(request.POST)
        context = {}
        if form.is_valid():
            search_query_from = form.cleaned_data['date_from']
            search_query_to = form.cleaned_data['date_to']
            place_of_visit = ALL_PLACES[int(form.cleaned_data['place'])][1]

           # doc_speciality = PHYSICIAN_SPECIALITIES[int(form.cleaned_data['doctor_speciality'])][0]
            booked_appt = Appointment.objects.get(id=appointment_2rotate_id)
            doc_speciality = booked_appt.doctor.speciality.all()

            # searching for the visit of the given parameters: free, date, place
            query_filter = {
                'date__range': [search_query_from, search_query_to],    # date can be searched for swap
                'place': Place.objects.get(name=place_of_visit)         # place can be changed for swap
            }

            # filtering appointments that meet the query_filter requirements
            appts_av_2swap = Rotation.objects.filter(user2=None)
            pk_list = [] #list of all appontments that meet the search_query except the one that the current user wants to swap
            for appt in appts_av_2swap:
                if appt.appointment_2rotate_id == appointment_2rotate_id: #appointment that current user wants to swap
                    pass
                else:
                    pk_list.append(appt.appointment_2rotate_id) # other appointments that meet the search query_filter

            appts_2swap = Appointment.objects.filter(pk__in=pk_list).\
                filter(**query_filter).order_by('date') # appointments that meet the criteria of search_query that are also in the Rotation table (available to be swapped)

            # building context to be rendered on the webpage
            context['appointment_booked'] = booked_appt
            context['search_query_from'] = search_query_from
            context['search_query_to'] = search_query_to
            context['doctor_speciality'] = doc_speciality[0]
            context['appointments_2swap'] = appts_2swap
        else:
            context['error_message'] = 'Error!'

        #the following code is for adding user2_id into Rotation table at the given appointment
        #appt_rotation - appointment that is in the Rotation table - other user posted for swap
        #appt_swap - appointment to swap with - current user asking to swap
        swap_visit_yes = request.POST.get('swap')
        if swap_visit_yes is not None:
            appt_rotation_id = int(swap_visit_yes[8:])
            appt_rotation = Rotation.objects.get(appointment_2rotate_id=appt_rotation_id)

            # if the user is logged in and pushed the button ask to swap then database change
            if swap_visit_yes == f'swap_me_{appt_rotation_id}' and request.user.id is not None:
                print(appt_rotation)
                appt_rotation.user2_id = request.user.id
                appt_rotation.save()
                messages.success(request, "Appointment sent to swap")
                return redirect("rotation:rotation_page")

        return render(request, 'rotation/rotations_found.html', context)


class RotationSwapView(View):
    def get(self, request):
        rotation_own = Rotation.objects.filter(user1=request.user.pk)
        rotation_else = Rotation.objects.filter(user2__isnull=False).filter(user1_agree=False)
        return render(request, "rotation/swap_list.html", {"rotation_own": rotation_own,
                                                           "rotation_else": rotation_else})

