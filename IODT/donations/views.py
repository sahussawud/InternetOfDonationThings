from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import FileInput, modelformset_factory
from django.forms.models import modelform_factory
from django.shortcuts import redirect, render

from donations.forms import DonationForm, PhotoForm
from donations.models import Album, Picture
from register.models import Doner


# Create your views here.
@login_required
def register_donations(request):
    contexts={}
    # Pictureformset = modelformset_factory(Picture, form=PhotoForm, fields=('url',), extra=3)
    if request.method == 'POST':
        # formset = Pictureformset(request.POST, request.FILES)
        form = DonationForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.donor = Doner.objects.get(user=settings.AUTH_USER_MODEL)
            # create album for pic
            if request.FILES.getlist('images'):
                album = Album(name='Album of ' + request.POST.get['name'])
                for file in request.FILES.getlist('images'):
                    pic = Picture(
                            name=request.POST.get['name'],
                            url=file,
                            album=album
                    )
                    pic.save()
                new_form.album = album
                new_form.save
                context['success'] = 'บันทึกสำเร็จ'
        else:
                context['danger'] = 'บันทึกไม่สำเร็จ'

    else:
        # formset = Pictureformset()
        form = DonationForm()

    contexts['form'] = form
    return render(request, 'donations/register_donations.html', context=contexts) 

def register(request):
    return redirect('register_donations')
