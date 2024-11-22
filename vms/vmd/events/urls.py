from django.contrib import admin
from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('admin/', admin.site.urls),
   path('', views.category_list, name='category_list'),
    path('create-category/', views.create_category, name='create_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category/<int:category_id>/', views.category_events, name='category_events'),
    path('create-event/', views.create_event, name='create_event'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
   path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event-chart/', views.event_chart, name='event_chart'),
]