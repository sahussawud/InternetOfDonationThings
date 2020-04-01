from django.urls import path
from register import views


urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name = 'my_logout'), 
    path('change_password/', views.ChangePassword, name = 'ChangePassword'), 
    path('step1/', views.register, name='register'),
    path('step2/', views.register2, name='register2'),
    # path('step1', views.step)
]  

 
