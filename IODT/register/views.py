from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required

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

        return redirect('index')