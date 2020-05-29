from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('project/<int:project_id>/', views.project_view, name='project_view'),
    path('project/manage/<int:project_id>/', views.project_management, name='project_management'),
    # path('login/', views.login, name='login'),

    path('api/project_summary/<int:project_id>/', views.project_summary_api.as_view(), name='project_summary_api'),
    path('api/change_status/', views.change_status, name='change_status'),
]
