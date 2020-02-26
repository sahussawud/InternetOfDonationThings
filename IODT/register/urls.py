from django.urls import path
from register import views

urlpatterns = [
    path('donor_form/', views.register, name='donor_form'),
    path('complete/', views.complete, name='complete'),
    path('', views.register, name='register'),
    
 
]