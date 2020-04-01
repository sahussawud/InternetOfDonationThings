from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def dashboard(request):
    return render(request, 'report/report.html')

def search(request):
    return HttpResponse('Attendance Search Page.')

def index(request):
    return render(request, 'report/index.html',{})