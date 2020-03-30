from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='class_search'),
    # path('login/', views.login, name='login'),
]