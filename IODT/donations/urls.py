from django.urls import path
from donations import views

urlpatterns = [
    path('register/', views.register_donations, name='register_donations'),
    # path('complete/', views.complete, name='complete'),
    path('mydonations/',views.donation_list, name='donation_list'),
    # path('activate/<int:id_thing>/',views.activate, name='activate'),
    path('project/create/', views.create_project, name='create_project')
]