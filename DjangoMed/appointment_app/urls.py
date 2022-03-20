from django.urls import path
from appointment_app.views import LoginView, log_out, \
    HomeView, AppFreeListView, AppSearchView, AppDetailsView

app_name = "appointment_app"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name="login"),
    path('logout', log_out, name="logout"),
    path('appointments/list/', AppFreeListView.as_view(), name='available_appointments'),
    path('appointments/search/', AppSearchView.as_view(), name='search_appointments'),
    path('appointments/search/details/<int:appointment_id>', AppDetailsView.as_view(), name='details_appointment'),
]