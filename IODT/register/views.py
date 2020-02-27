from django.shortcuts import redirect, render
from django.template.context_processors import request
from .models import thing
from .forms import thingForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

# Create your views here.
def complete(request):
    print(request)
    return render(request, 'register/reg_complete.html',  context={
        'name': request.POST.get('name'),
        'address' : request.POST.get('address'),
        'reciever' : request.POST.get('reciever')
    })

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
        thing_pk = things.pk
        return HttpResponseRedirect(reverse('complete', kwargs={'thing_id':thing_pk,'name': names, 'address': addresss, 'reciever': recievers}))
        # return redirect(to='complete', kwargs={'name': names, 'address': addresss, 'reciever': recievers})
    return render(request, 'register/register.html')


def activate(request, id_thing):
    print(id_thing)
    a_thing = thing.objects.get(pk=id_thing)
    contexts = {
        'name': a_thing.name,
        'address': a_thing.address,
        'reciever': a_thing.reciever,
        'thing_id': a_thing.pk
    }
    return render(request, 'register/activate.html',context=contexts)
     
def donor_form(request):
    return render(request, 'register/donor_form.html')