from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from donations.models import Donation, Project

from django.contrib.messages import success

# Create your views here.

@login_required
def add_donation_to_project(request, donation_id, project_id):
    donation = Donation.objects.get(pk=donation_id)
    ref_project = Project.objects.get(pk=project_id)
    donation.project = ref_project
    #Set stutus to pending 
    donation.status = Donation.STATUS[1][0]
    donation.save()
    success(request, donation.name+' ถูกลงทะเบียนไปที่ '+ref_project.name+' สำเร็จ')
    return redirect('donation_list')

