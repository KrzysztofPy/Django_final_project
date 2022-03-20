from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from appointment_app.models import Patient, Appointment

from appointment_app.forms import AppSearchForm, LoginForm


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


class AppFreeListView(View):
    # This class view is for listing all appointments that are available/free to book for all users
    def get(self, request):
        free_appts = Appointment.objects.filter(user=None)
        context = {
            'fappts': free_appts
        }
        return render(request, 'list_free_appts.html', context)


class AppSearchView(View):
    def get(self, request):
        form = AppSearchForm()
        return render(request, 'search_free_appts.html', {'form': form})

    def post(self, request):
        form = AppSearchForm(request.POST)
        context = {}
        if form.is_valid():
            search_query = form.cleaned_data['date']
            appts = Appointment.objects.filter(date=search_query).filter(user=None)
            context['search_query'] = search_query
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
        book_visit_yes = request.POST.get('book_yes')
        search_again = request.POST.get('search_new')
        #if the user pushed the button to book visit then database change
        if book_visit_yes == 'book_me':
            appt = Appointment.objects.get(pk=appointment_id)
            #appt.user
        return HttpResponse(f'{appointment_id}, {book_visit_yes}, {search_again}')