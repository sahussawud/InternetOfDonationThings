from django.urls import path
from register import views

urlpatterns = [
    path('donor_form/', views.register, name='donor_form'),
    path('complete/', views.complete, name='complete'),
    path('activate/<int:id_thing>/',views.activate, name='activate'),
    path('', views.register, name='register')
]

 
