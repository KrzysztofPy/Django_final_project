from django.urls import path

from login.views import LoginView, log_out

app_name = "login_app"

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', log_out, name="logout"),
]
