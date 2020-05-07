
import base64
import json
import random
from builtins import object
from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import FileInput, modelformset_factory
from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse

import pyqrcode
from donations.forms import CreateProjectForm, DonationForm, FeedbackForm
from donations.models import Album, Donation, Location, Picture, Project, Feedback
from register.models import Doner, Recipient

from .models import Qrcode

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from donations.serializers import *

# Create your views here.
@login_required
def project_select(request, donation_id):
    contexts={}
    donation = Donation.objects.get(pk=donation_id)
    donation_picture = Picture.objects.filter(album=donation.album)
    # Retrieve only project that the same requiretype
    project = Project.objects.filter(requiretype__id=donation.dtype.id)
    print(project)
    contexts['donation'] = donation
    contexts['donation_picture'] = donation_picture[0]
    contexts['projects'] = project
    return render(request, 'donations/project_select.html', context=contexts) 

@login_required
def register_donations(request):
    contexts={}
    # Pictureformset = modelformset_factory(Picture, form=PhotoForm, fields=('url',), extra=3)
    if request.method == 'POST':
        # formset = Pictureformset(request.POST, request.FILES)
        form = DonationForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            Name = request.POST.get('name')[:3]
            new_form.donor = Doner.objects.get(user=request.user)
            # create album for pic
            if request.FILES.getlist('images'):
                album = Album(name='Album of ' + Name)
                album.save()
                for file in request.FILES.getlist('images'):
                    pic = Picture(
                            name=Name,
                            url=file,
                            album=album
                    )
                    pic.save()
            new_form.album = album
            new_form.save()
            contexts['success'] = 'บันทึกสำเร็จ'
        else:
            contexts['danger'] = 'บันทึกไม่สำเร็จ'
            form = DonationForm()

    else:
        # formset = Pictureformset()
        form = DonationForm()

    contexts['form'] = form
    return render(request, 'donations/register_donations.html', context=contexts) 

@login_required
def project_list(request):
    contexts={}
    recipient = Recipient.objects.get(user=request.user)
    myproject = Project.objects.filter(recipient=recipient).order_by('create_date','name')
    contexts['recipient'] = recipient
    contexts['projects'] = myproject
    return render(request, 'donations/project_list.html', context=contexts) 

@login_required
def donation_list(request):
    contexts={}
    Doner_ = Doner.objects.get(user=request.user)
    mydonation = Donation.objects.filter(donor=Doner_).order_by('date','name')
    contexts['doner'] = Doner_
    contexts['mydonation'] = mydonation
    return render(request, 'donations/donation_list.html', context=contexts) 

@login_required
def create_project(request):
    contexts = {}
    if request.method == 'POST':
        # formset = Pictureformset(request.POST, request.FILES)
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            Name = request.POST.get('name')[:3]
            new_form.recipient = Recipient.objects.get(user=request.user)
            # create album for pic
            if request.FILES.getlist('images'):
                print(request.FILES.getlist('images'))
                album = Album(name='Album of ' + Name)
                album.save()
                for file in request.FILES.getlist('images'):
                    pic = Picture(
                            name=Name,
                            url=file,
                            album=album
                    )
                    pic.save()
            new_form.album = album
            new_form.status = Project.STATUS[0][0]
            new_form.save()
            # save RequireType to m2m has to save after create an instance
            form.save_m2m()
            contexts['success'] = 'บันทึกสำเร็จ'
        else:
            contexts['danger'] = 'บันทึกไม่สำเร็จ'
            form = CreateProjectForm()

    else:
        form = CreateProjectForm()

    contexts['form'] = form
    return render(request, 'donations/register_project.html', context=contexts)


@login_required
def tracking(request, donation_id):
    contexts={}
    #retrieve object donation
    donation = Donation.objects.get(pk=donation_id)
    pictures = Picture.objects.filter(album=donation.album)
    feedback = Feedback.objects.filter(donation=donation_id)
    feedback_w_photo = []
    for item in feedback:
        print(item)
        photos =  Picture.objects.filter(album=item.album)
        f_w_p = {'photos':photos, 'contents':item}
        feedback_w_photo.append(f_w_p)
    contexts['feedback'] = feedback_w_photo
    encoded = None
    #check that doantion has register with qrcode yet?
    try:
        qrcode = Qrcode.objects.get(donation=donation)
        number = pyqrcode.create(request.build_absolute_uri(reverse('feedback_by_qrcode', kwargs={'hash_id':qrcode.value})))
        s = BytesIO()
        number.png(s,scale=60)
        #encode to Base64 image
        encoded = base64.b64encode(s.getvalue()).decode("ascii")
        
    except ObjectDoesNotExist:
        qrcode = None
        print('Binding QrCode Not found')
        #generate MD5 hash id
        qrcode_id = ''
        while True:
            hash = random.getrandbits(128)
            qrcode_id = "%032x" % hash
            try:
                qrcode = Qrcode.objects.get(value=qrcode_id)
                print('Random New Hash')
            except ObjectDoesNotExist:
                print('Random New Hash is %s' % qrcode_id)
                break

        
        #create qrcode
        number = pyqrcode.create(request.build_absolute_uri(reverse('feedback_by_qrcode', kwargs={'hash_id':qrcode_id})))
        s = BytesIO()
        number.png(s,scale=100)
        #encode to Base64 image
        encoded = base64.b64encode(s.getvalue()).decode("ascii")
        contexts['qrcode'] = {
            'hash': qrcode_id,
            'encoded' : encoded,
        }

    contexts['information'] = {
        'pictures' : pictures,
        'data' : donation,
        'qrcode': qrcode,
        'link_qrcode': encoded
    }

    contexts['map'] = {
        'id': 1,
        'title': 'โครงการทดลอง',
        'pic': 'https://www.csc.gov.sg/images/default-source/ethos-images/ethos-digital-issue-3/charity_754x556px.jpg',
        'desc': 'โครงการเสื้อการกุศล " กำลังใจนักสู้ " ปัญหาความไม่สงบในสามจังหวัดชายแดนภาคใต้ตลอดหลายสิบปีที่ผ่านมาได้คร่าชีวิตประชาชนและเจ้าหน้าที่ผู้ปฏิบัติงาน',
        'project': '/project/1/',
        'location':{'lat':'7.33759', 'lng':'100.47862'},
        'type': 'เด็กสาว',
        'icon': 'IconGirl',
    }
    return render(request, 'donations/tracking.html', context=contexts) 

def qrcode_binding(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        donation = Donation.objects.get(pk=int(data['donation']))
        qrcode = Qrcode.objects.create(
            donation = donation,
            use_flag = True,
            value = data['hash']
        )
        return HttpResponse(status=201)
    return HttpResponse(status=405)

def qrcode_delete(request, qrcode_id):
    if request.method == 'DELETE':
        qrcode = Qrcode.objects.get(pk=qrcode_id)
        qrcode.delete()
        return HttpResponse(status=200)
        return redirect('tracking')
    return HttpResponse(status=405)

def feedback_by_qrcode(request, hash_id):
    contexts = {}
    try:
        qrcode = Qrcode.objects.get(value=hash_id)
        pic = Picture.objects.filter(album=qrcode.donation.album)
        contexts['donation'] = qrcode.donation
        contexts['pictures'] = pic
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            Name = request.POST.get('header')[:3]
            ladtitude = request.POST.get('ladtitude')
            longtitude = request.POST.get('longtitude')
            print("ladtitude longtitude ",ladtitude, longtitude)
            if form.is_valid():
                newform = form.save(commit=False)
                if request.FILES.getlist('images'):
                    print(request.FILES.getlist('images'))
                    album = Album(name='Album of ' + Name)
                    album.save()
                    for file in request.FILES.getlist('images'):
                        pic = Picture(
                                name=Name,
                                url=file,
                                album=album
                        )
                        pic.save()    
                    newform.album = album
                if ladtitude and longtitude:
                    location = Location.objects.create(name=Name,
                                                        _type='feedback',
                                                        ladtitude=ladtitude,
                                                        longtitude=longtitude)
                    newform.location = location
                    print(location)

                newform.donation = qrcode.donation
                newform.save()
                messages.success(request, 'สง่ข้อความสำเร็จ.')
            else:
                form = FeedbackForm(request.POST)
                messages.error(request, 'กรุณากรอกข้อความใหม่.')
        else:
            form = FeedbackForm()

    except Qrcode.DoesNotExist:
        messages.error(request, 'QR not found.')
        form = FeedbackForm()

    contexts['hash_id'] = hash_id
    contexts['form'] = form
    return render(request, 'donations/feedback_by_qrcode.html',context=contexts)

def test_map (request):
    if request.method == 'DELETE':
        print('test_pass')
        return HttpResponse(status=200)

class feedback_api(APIView):
    """ API ดึง feedback ทั้งหมดของ donation นั้น
        ส่ง donor id ทาง params มา รหัสผู้บริจาค"""
    def get(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        feeddback = Feedback.objects.filter(donation=donation)
        serializer = FeedbackSerializer(feeddback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class last_location_of_donation(APIView):
#     """ API ดึง location ล่าสุดของของบริจาคทั้งหมด """
#     def get(self, request):
#         if request.GET.get('donor_id'):
#             donor = Doner.objects.get(id=request.GET.get('donor_id'))
#             donation = Donation.objects.filter(donor=donor)
#             feedback = Feedback.objects.filter(donation=donation)
#             serializer = FeedbackSerializer(feedback, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

