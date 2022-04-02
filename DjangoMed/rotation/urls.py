from django.urls import path

from rotation.views import HomeView

app_name = "rotation"

urlpatterns = [
    path('rotation/', HomeView.as_view(), name='home'),
]
