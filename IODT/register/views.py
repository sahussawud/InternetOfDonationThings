from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from register.forms import regForm
from register.models import *

@login_required
def ChangePassword(request):
    context={}
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password')
        re_password = request.POST.get('password_again')

        if password != re_password:
            context['error'] = 'Password do not match'
        else:
            u = user.objects.get(username=username)
            u.set_password(password)
            u.save()
            context['success'] = 'Change Password Successfully'
            return redirect('my_logout')

    return render(request, 'register/changepassword.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('index')

def my_login(request): # function login base django
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next')
            print(next_url)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context = {
                'username': username,
                'error': 'Wrong username or password'
            }

    return render(request, 'register/my_login.html',context=context)

def register(request):
    # if request.user.is_authenticated:
    #     my_logout(request)
    context = {}
    context['list_open_row'] = ["username", "first_name", "email"]
    context['list'] = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]
    context['list_close_row'] = ["password2", "last_name", "phone"]

    if request.method == 'POST':
        form = regForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('register2')
    else:
        form = regForm()
        context['form'] = form

    return render(request, 'register/register.html', context)

def register2(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        form_name = request.POST.get('form_name')
        sex = request.POST.get('sex')

        if sex == 'other':
            sex = request.POST.get('sex_other')

        if form_name == 'donor_form':
            donor_form = Doner(
                user = request.user,
                sex = sex[0],
                donate_amount = 0,
                helping_amount = 0
            )
            user.address = request.POST.get('address')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            donor_form.save()

        else:
            recipient_form = Recipient(
                user = request.user,
                rating = 0,
                response_rate = 0,
                desc = request.POST.get('description')
            )
            recipient_form.save()
            recipient_form = Recipient.objects.filter(user=request.user.id)[0]

            if form_name == 'recipient_form_organization':
                recipient_form_organization = Organization(
                    recipient = recipient_form,
                    name = request.POST.get('organization_name'),
                    establish_date = request.POST.get('establish_date'),
                    vision = request.POST.get('vision')
                )
                user.address = request.POST.get('address')
                user.save()
                recipient_form_organization.save()

            if form_name == 'recipient_form_person':
                recipient_form_person = People(
                    recipient = recipient_form,
                    sex = sex[0]
                )
                user.address = request.POST.get('address')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.save()
                recipient_form_person.save()
        return redirect('profile')
    return render(request, 'register/register2.html', context)

@login_required
def my_profile(request):
    user = request.user
    donor = Doner.objects.filter(user_id=user.id)
    recipient = Recipient.objects.filter(user_id=user.id)
    context = {
        'username': user.username,
        'profile_pic': user.profile_pic
    }
    if donor:
        donor = donor[0]
        context = {
            'type': 'donor',
            'username': user.username,
            'profile_pic': user.profile_pic,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'sex': donor.sex,
            'email': user.email,
            'phone': user.phone,
            'create_date': user.date_joined.strftime("%d / %m / %Y"),
            'address': user.address
        }
    if recipient:
        recipient = recipient[0]
        recipient_organization = Organization.objects.filter(recipient_id=recipient.id)
        recipient_people = People.objects.filter(recipient_id=recipient.id)
        if recipient_organization:
            recipient_organization = recipient_organization[0]
            context = {
                'type': 'recipient_organization',
                'username': user.username,
                'profile_pic': user.profile_pic,
                'email': user.email,
                'phone': user.phone,
                'create_date': user.date_joined.strftime("%d / %m / %Y"),
                'address': user.address,
                'description': recipient.desc,
                'organization_name': recipient_organization.name,
                'establish_date': recipient_organization.establish_date.strftime("%d / %m / %Y"),
                'vision': recipient_organization.vision
            }
        if recipient_people:
            recipient_people = recipient_people[0]
            context = {
                'type': 'recipient_people',
                'username': user.username,
                'profile_pic': user.profile_pic,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'sex': recipient_people.sex,
                'email': user.email,
                'phone': user.phone,
                'create_date': user.date_joined.strftime("%d / %m / %Y"),
                'address': user.address,
                'description': recipient.desc
            }

    return render(request, 'register/profile.html', context)

def tracking_test(request):
    context = {}
    return render(request, 'tracking_test.html', context)