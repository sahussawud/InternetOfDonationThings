from django.shortcuts import redirect, render
from django.template.context_processors import request
from .forms import RegThingForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    context=dict()
    if request.method == "POST":
        context = {
            'name' : request.POST.get('title'),
            'reciever' : request.POST.get('reciever'),
            'address' : request.POST.get('address'),
            'is_accept' : request.POST.get('is_accept'),
            'picture' : request.POST.get('picture')
        }
        return render(request, 'register/register.html',context)
    return render(request, 'register/register.html')

def complete(request):
    print(request.POST)
    return render(request, 'register/reg_complete.html')

def donor_form(request):
    return render(request, 'register/donor_form.html')