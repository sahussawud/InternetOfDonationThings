from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:donation_id>/<int:project_id>',views.add_donation_to_project, name='add_donation_to_project'),
    
]