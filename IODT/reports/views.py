from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def login(request): # function login base django
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('../index/')
        else:
            context = {
                'username': username,
                'error': 'Wrong username or password'
            }
    return render(request, template_name='', context=context)

def dashboard(request):
    return render(request, 'report/report.html')

def search(request):
    return HttpResponse('Attendance Search Page.')

def index(request):
    return render(request, 'report/index.html',{})