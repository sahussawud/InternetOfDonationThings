from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('project/<int:project_id>/', views.project_view, name='project_view'),
    path('project/manage/<int:project_id>/', views.project_management, name='project_management'),
    # path('login/', views.login, name='login'),
]
