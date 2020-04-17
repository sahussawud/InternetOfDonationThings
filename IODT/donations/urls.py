from django.urls import path
from donations import views

urlpatterns = [
    path('register/', views.register_donations, name='register_donations'),
    # path('complete/', views.complete, name='complete'),
    path('mydonations/',views.donation_list, name='donation_list'),
    path('project/<int:donation_id>/add',views.project_select, name='project_select'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/my/', views.project_list, name='project_list'),
    path('tracking/<int:donation_id>', views.tracking, name='tracking'),
    path('api/qrbinding/', views.qrcode_binding, name='qrbinding'),
    path('api/qrcode_delete/<int:qrcode_id>', views.qrcode_delete, name='qrcode_delete')
]