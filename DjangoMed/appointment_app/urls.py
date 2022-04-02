from django.urls import path
from appointment_app.views import HomeView, AppFreeListView, AppBookedListView, \
    AppSearchView, AppDetailsView, AppBookedView, AppAddView, ShowDoctorsView, ShowSpecialitiesView

app_name = "appointment_app"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('doctors/list', ShowDoctorsView.as_view(), name='shows_doctors'),
    path('specialities/list', ShowSpecialitiesView.as_view(), name='shows_specialities'),
    path('appointments/list/', AppFreeListView.as_view(), name='available_appointments'),
    path('appointments/booked/list/', AppBookedListView.as_view(), name='booked_appointments'),
    path('appointments/search/', AppSearchView.as_view(), name='search_appointments'),
    path('appointments/search/details/<int:appointment_id>', AppDetailsView.as_view(), name='details_appointment'),
    path('appointments/booked/all/', AppBookedView.as_view(), name='list_all_booked_appointments'),
    path('appointments/add/', AppAddView.as_view(), name='add_appointment'),
]