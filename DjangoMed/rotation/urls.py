from django.urls import path

from rotation.views import HomeView, RotationSearchView

app_name = "rotation"

urlpatterns = [
    path('rotation/', HomeView.as_view(), name='home'),
    path('rotation/search/<int:appointment_2rotate_id>', RotationSearchView.as_view(), name='rotation_search'),
]
