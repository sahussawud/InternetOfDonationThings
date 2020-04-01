from django.urls import path
from register import views


urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name = 'my_logout'), 
    path('change_password/', views.ChangePassword, name = 'ChangePassword'), 
]  

 
