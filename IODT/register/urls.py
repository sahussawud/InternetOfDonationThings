from django.urls import path
from register import views

urlpatterns = [
    path('donor_form/', views.donor_form, name='donor_form'),
    path('', views.register, name='register'),
    path('complete/', views.complete, name='complete')
 
]