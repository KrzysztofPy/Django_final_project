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
from appointment_app.models import Appointment, Patient, PHYSICIAN_SPECIALITIES, Place, PhysicianSpeciality

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

            doc_speciality = PHYSICIAN_SPECIALITIES[int(form.cleaned_data['doctor_speciality'])][0]
            booked_appt = Appointment.objects.get(id=appointment_2rotate_id)
            doc_speciality = booked_appt.doctor.speciality
            # searching for the visit of the given parameters: free, date, place
            query_filter = {
                'date__range': [search_query_from, search_query_to],
                # 'doctor': Doctor.objects.filter(pk__in=doctors_list),
                # 'doctor': Doctor.objects.filter(speciality=doc_speciality).all(),
                # 'doctor': Doctor.objects.filter(pk__in=doctors_list),
                'place': Place.objects.get(name=place_of_visit)
            }
            # filtering appointments that meet the query_filter requirements
            appts_av_2swap = Rotation.objects.filter(user2=None)
            pk_list = [] #list of all appontments that meet the search_query
            for appt in appts_av_2swap:
                if appt.appointment_2rotate_id == appointment_2rotate_id:
                    pass
                else:
                    pk_list.append(appt.appointment_2rotate_id)
            print(pk_list)
            appts_2swap = Appointment.objects.filter(pk__in=pk_list).\
                filter(**query_filter).\
                order_by('date') # appointments that meet the criteria of search_query that are also in the Rotation table (available to be swapped)
            #appts = Appointment.objects.filter(**query_filter).order_by('date')
            # building context to be rendered on the webpage
            context['search_query_from'] = search_query_from
            context['search_query_to'] = search_query_to
            context['appointments_2swap'] = appts_2swap
        else:
            context['error_message'] = 'Error!'
        return render(request, 'rotation/rotations_found.html', context)


    """        #appts_2swap = Rotation.objects.all().except(appointment_2rotate_id=appointment_2rotate_id)
        """


