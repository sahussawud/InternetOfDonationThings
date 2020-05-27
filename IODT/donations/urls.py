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
    path('api/qrcode_delete/<int:qrcode_id>', views.qrcode_delete, name='qrcode_delete'),
    path('feedback/<str:hash_id>/', views.feedback_by_qrcode, name='feedback_by_qrcode'),
    path('track_donations/', views.track_donations, name='track_donations'),

    path('api/feedback/donation/<int:donation_id>/', views.feedback_api.as_view(), name='feedback_api'),
    path('api/project/', views.project_api.as_view(), name='project_api'),
    path('api/requiretype/', views.requiretype_api.as_view(), name='requiretype_api'),


]