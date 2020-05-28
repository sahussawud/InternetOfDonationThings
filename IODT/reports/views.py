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
from donations.serializers import ProjectSummarySerializer

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
    """ API ดึงข้อมูลสรุปทั้งหมดของ ของโปรเจค โดย รับ Project_id ทาง path 
        สามารถ patch สถานะโครงการได้"""
    def get(self, request, project_id):
        """ ส่งข้อมูลสรุปไป """
        project = Project.objects.get(id=project_id)
        print(project)
        serializer = ProjectSummarySerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request, project_id):
        """ ส่งข้อมูลสรุปไป """
        project = Project.objects.get(id=project_id)
        serializer = ProjectSummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            item = Project.objects.get(id=project_id)
            serializer = ProjectSummarySerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)