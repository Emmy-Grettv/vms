from django.contrib import admin
from django.urls import path
from . import views

app_name = 'volunteers'


urlpatterns = [
    path('', views.login_view),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
   path('logout/', views.logouts, name='logout'),

    






  
     


    


]
