from django.urls import path
from .views import ParticipationListView

urlpatterns = [
    path('', ParticipationListView.as_view(), name='participations'),
]
