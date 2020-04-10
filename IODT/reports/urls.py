from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/', views.project_view, name='project_view'),
    # path('login/', views.login, name='login'),
]
