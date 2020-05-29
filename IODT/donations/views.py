
import base64
import json
import random
from builtins import object
from io import BytesIO
from datetime import date

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
from donations.models import Album, Donation, Location, Picture, Project, Feedback, RequireType
from register.models import Doner, Recipient

from .models import Qrcode
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from donations.serializers import *
from django.db.models import Count

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
            messages.success(request, 'ลงทะเบียน '+new_form.name+' สำเร็จ')
            return redirect('donation_list')
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
    donation_cp = []   
    for item in mydonation:
        print(item)
        photos =  Picture.objects.filter(album=item.album)
        f_w_p = {'photos':photos, 'contents':item}
        donation_cp.append(f_w_p)

    contexts['doner'] = Doner_
    contexts['mydonation'] = donation_cp
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
    print(form)
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
                messages.success(request, 'ส่งข้อความสำเร็จ.')
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

def track_donations (request):
    contexts = {}
    return render(request, 'donations/track_donations.html',context=contexts)

class feedback_api(APIView):
    """ API ดึง feedback ทั้งหมดของ donation นั้น
        ส่ง donor id ทาง params มา รหัสผู้บริจาค"""
    def get(self, request, donation_id):
        """ IF กรณีต้องการจะดูทั้งหมดจะส่ง id_donation = 0 มา """
        if donation_id != 0:
            donation = Donation.objects.get(id=donation_id)
            feeddback = Feedback.objects.filter(donation=donation)
        else:
            feeddback = Feedback.objects.all().order_by("donation")
        serializer = FeedbackSerializer(feeddback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class project_api(APIView):
    """ API ดึง โครงการ เพื่อดูสำหรับเข้าไปบริจาคทื่หน้าหลัก
        สามารถที่จะ search ได้ ทั้ง category search เเละ keyword
        ผ่าน params requiretype(ตามไอดีของ requiretype ที่อยู่ใน db)
                    ,keyword(คำค้นหา), all_select(ทั้งหมด หรือ เอาเเค่ที่ยังไม่ปิดรับ)
        """
    def get(self, request):
        """requiretype = id"""
        requiretype = request.GET.get('requiretype')
        keyword = request.GET.get('keyword')
        active_project = request.GET.get('active_project')
        """ถ้ามีการเลือกประเภท"""
        if requiretype:
            """มีการใส่keyword"""
            requiretype_ob = RequireType.objects.get(id=requiretype)
            if keyword:
                project = Project.objects.filter(Q(requiretype=requiretype_ob),
                                                Q(name__contains=keyword) | Q(desc__contains=keyword))
            else:
                project = Project.objects.filter(requiretype=requiretype_ob)
        else:
            """ถ้าไม่มีการเลือกประเภท"""
            if keyword:
                project = Project.objects.filter(Q(name__contains=keyword) | Q(desc__contains=keyword))
            else:
                project = Project.objects.all()
        if active_project:
            project = project.filter(expire_date__gte=date.today())

        project = project.order_by('expire_date')
        serializer = ProjectOverviewSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class requiretype_api(APIView):
    def get(self, request):
        requiretype_ob = RequireType.objects.all()
        serializer = RequireTypeSerializer(requiretype_ob, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


