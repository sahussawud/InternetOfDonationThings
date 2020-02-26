from django.shortcuts import redirect, render
from django.template.context_processors import request
from .models import thing
from .forms import thingForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def complete(request):
    print(request.POST)
    return render(request, 'register/reg_complete.html')
    
def register(request):
    if request.method == 'POST':
        names = request.POST.get('name')
        addresss = request.POST.get('address')
        is_accepts = request.POST.get('is_accept')
        pics = request.POST.get('picture')
        recievers = request.POST.get('reciever')

        things = thing(
            name = names,
            address = addresss,
            picture = pics,
            reciever = recievers
        )
        things.save()
        redirect('complete')
    return render(request, 'register/register.html', )


def donor_form(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = thingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            
            # ...
            # redirect to a new URL:        
            redirect('complete')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = thingForm()

    return render(request, 'register/donor_form.html', context={'form': form})