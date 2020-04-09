
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import FileInput, modelformset_factory
from django.forms.models import modelform_factory
from django.shortcuts import redirect, render
from django.template.context_processors import request

from donations.forms import CreateProjectForm, DonationForm
from donations.models import Album, Donation, Picture, Project
from register.models import Doner, Recipient


# Create your views here.
@login_required
def project_select(request, donation_id):
    contexts={}
    donation = Donation.objects.get(pk=donation_id)
    # Retrieve only project that the same requiretype
    project = Project.objects.filter(requiretype=donation.dtype)
    print(project)
    contexts['donation'] = donation
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
            contexts['success'] = 'บันทึกสำเร็จ'
        else:
            contexts['danger'] = 'บันทึกไม่สำเร็จ'
            form = CreateProjectForm()

    else:
        form = CreateProjectForm()

    contexts['form'] = form
    return render(request, 'donations/register_project.html', context=contexts)
