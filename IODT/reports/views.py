from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from donations.models import Project, Donation, Album, Picture
from register.forms import regForm
from register.models import Organization
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

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
    context['form'] = regForm()
    return render(request, 'report/index_2.html', context)

def project_view(request, project_id):
    contexts = {}
    project = Project.objects.get(pk=project_id)
    project_picture = Picture.objects.filter(album=project.album)
    donation_in_project = Donation.objects.filter(project=project)
    contexts['project'] = project
    contexts['project_picture'] = project_picture
    contexts['project_in_project'] = donation_in_project
    return render(request, 'report/project_view.html',context=contexts)

@login_required
def project_management(request, project_id):
    contexts = {}
    project = Project.objects.get(pk=project_id)
    project_picture = Picture.objects.filter(album=project.album)
    donation_in_project = Donation.objects.filter(project=project)
    contexts['project'] = project
    contexts['project_picture'] = project_picture
    contexts['project_in_project'] = donation_in_project
    return render(request, 'report/project_management.html',context=contexts)

class project_summary_api(APIView):
    """ API ดึง feedback ทั้งหมดของ donation นั้น
        ส่ง donor id ทาง params มา รหัสผู้บริจาค"""
    def get(self, request, project_id):
        """ IF กรณีต้องการจะดูทั้งหมดจะส่ง id_donation = 0 มา """
        if donation_id != 0:
            donation = Donation.objects.get(id=donation_id)
            feeddback = Feedback.objects.filter(donation=donation)
        else:
            feeddback = Feedback.objects.all()
        serializer = FeedbackSerializer(feeddback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)