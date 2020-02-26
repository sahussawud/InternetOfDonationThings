from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'report/report.html')

def search(request):
    return HttpResponse('Attendance Search Page.')

def index(request):
    return render(request, 'report/index.html')