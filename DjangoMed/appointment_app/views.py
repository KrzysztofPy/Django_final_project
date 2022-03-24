from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from appointment_app.models import Patient, Appointment

from appointment_app.forms import AppSearchForm, LoginForm, AppAddForm, HOURS, MINUTES

import datetime


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name, {"form": LoginForm})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("appointment_app:home")
        return render(request, self.template_name, {"form": LoginForm(request.POST)})


@login_required
def log_out(request):
    logout(request)
    return redirect("appointment_app:home")


class AppAddView(View):
    def get(self, request):
        form = AppAddForm()
        return render(request, "add_appointments.html", {"form":form})

    def post(self, request):
        form = AppAddForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time_h = int(HOURS[int(form.cleaned_data['time_hour'])][1])
            time_m = int(MINUTES[int(form.cleaned_data['time_minute'])][1])
            #return HttpResponse(f'{date}, {time_h}:{time_m}, {datetime.time(time_h, time_m, 0)}')
            Appointment.objects.create(date=date, time=datetime.time(time_h, time_m, 0))
            messages.success(request, "Appointment added")
        return redirect("appointment_app:add_appointment")


class AppFreeListView(View):
    # This class view is for listing all appointments that are available/free to book for all users
    def get(self, request):
        free_appts = Appointment.objects.filter(user=None).order_by('date')
        context = {
            'fappts': free_appts
        }
        return render(request, 'list_free_appts.html', context)


class AppBookedListView(View):
    def get(self, request):
        booked_appts = Appointment.objects.filter(user=request.user.id)
        return render(request, 'list_booked_appts.html', {'bappts': booked_appts})


class AppSearchView(View):
    def get(self, request):
        form = AppSearchForm()
        return render(request, 'search_free_appts.html', {'form': form})

    def post(self, request):
        form = AppSearchForm(request.POST)
        context = {}
        if form.is_valid():
            search_query_from = form.cleaned_data['date_from']
            search_query_to = form.cleaned_data['date_to']
            appts = Appointment.objects.filter(date__range=[search_query_from, search_query_to]).filter(user=None).order_by('date')
            context['search_query_from'] = search_query_from
            context['search_query_to'] = search_query_to
            context['appointments'] = appts
        else:
            context['error_message'] = 'Error!'
        return render(request, 'search_free_appts.html', context)


class AppDetailsView(View):
    #rendering html to show the details of the visit, two buttons available: Book visit and Search new
    def get(self, request, appointment_id):
        appt_detail = Appointment.objects.get(pk=appointment_id)
        return render(request,
                      "detail_appt.html",
                      {
                          'appt_detail': appt_detail
                      })

    #receiving data from form
    def post(self, request, appointment_id):
        #mapping buttons values to variables. Pressed button will change value from None to book_me or search
        book_visit_yes = request.POST.get('book_yes')
        search_again = request.POST.get('search_new')
        cancel_visit = request.POST.get('cancel')
        #if the user is logged in and pushed the button to book visit then database change
        if book_visit_yes == 'book_me' and request.user.id is not None:
            appt = Appointment.objects.get(pk=appointment_id)
            appt.user_id = request.user.id
            appt.save()
            messages.success(request, "Appointment booked")
            return redirect("appointment_app:booked_appointments")
        #if the user is not logged in then redirect to login page
        elif book_visit_yes == 'book_me' and request.user.id is None:
            messages.success(request, "You need to be logged in to book visits")
            return redirect("appointment_app:login")
        #if the search button is pressed then redirect to search_appointment page
        elif search_again == 'search':
            return redirect("appointment_app:search_appointments")
        #if the user pushes cancel buttun then the appointment record changes its column user_id to None
        elif cancel_visit == 'cancel_me':
            appt_to_cancel = Appointment.objects.get(pk=appointment_id)
            appt_to_cancel.user_id = None
            appt_to_cancel.save()
            messages.success(request, "Appointment cancelled")
            return redirect("appointment_app:booked_appointments")
        else:
            return HttpResponse(f'Error occurred!')


class AppBookedView(View):
    def get(self, request):
        appts_booked = Appointment.objects.exclude(user_id=None).order_by('date')
        return render(request, "all_booked_appointments.html", {'appointments': appts_booked})
