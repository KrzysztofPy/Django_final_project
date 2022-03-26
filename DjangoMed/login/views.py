from django.shortcuts import render, redirect

from django.views.generic import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from login.forms import LoginForm


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
