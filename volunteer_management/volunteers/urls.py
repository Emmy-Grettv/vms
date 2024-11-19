from django.urls import path
from .views import VolunteerListView, VolunteerDetailView

urlpatterns = [
    path('volunteers/', VolunteerListView.as_view(), name='volunteer-list'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
]
