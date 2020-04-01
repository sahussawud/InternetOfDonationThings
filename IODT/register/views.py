from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from register.forms import regForm

@login_required
def ChangePassword(request):
    context={}
    if request.method == 'POST':
        user = request.user.username
        password = request.POST.get('password')
        re_password = request.POST.get('password_again')

        if password != re_password:
            context['error'] = 'Password do not match'
        else:
            u = User.objects.get(username=user)
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
            next_url = request.POST.get('next_url')
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
    context = {}
    context['list_open_row'] = ["username", "first_name", "email"]
    context['list'] = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]
    context['list_close_row'] = ["password2", "last_name", "phone"]

    if request.method == 'POST':
        form = regForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = regForm()
        context['form'] = form

    return render(request, 'register/register.html', context)

    