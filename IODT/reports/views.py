from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from donations.models import Project, Donation, Album, Picture

# Create your views here.

def dashboard(request):
    return render(request, 'report/report.html')

def search(request):
    return HttpResponse('Attendance Search Page.')

def index(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        context[user] = request.user
    return render(request, 'report/index_2.html',{})

def project_view(request, project_id):
    contexts = {}
    project = Project.objects.get(pk=project_id)
    project_picture = Picture.objects.filter(album=project.album)
    donation_in_project = Donation.objects.filter(project=project)
    print(project)
    print(project_picture)
    print(donation_in_project)

    contexts['project'] = project
    contexts['project_picture'] = project_picture
    contexts['project_in_project'] = donation_in_project
    return render(request, 'report/project_view.html',context=contexts)