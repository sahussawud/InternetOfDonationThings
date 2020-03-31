from django.urls import path
from donations import views

urlpatterns = [
    path('donations/', views.register_donations, name='register_donations'),
    path('complete/', views.complete, name='complete'),
    path('activate/',views.activate_list, name='activate_list'),
    path('activate/<int:id_thing>/',views.activate, name='activate'),
    path('', views.register, name='register')
]