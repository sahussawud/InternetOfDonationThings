from django.shortcuts import redirect, render
from django.forms import modelformset_factory, FileInput
from donations.forms import DonationForm
from donations.models import Picture


# Create your views here.
def register_donations(request):
    Pictureformset = modelformset_factory(Picture, fields=('url',), extra=3, labels={'url':'เลือกรูปภาพ'},
                                         widgets={'name': FileInput(attrs={'class': 'file'})})
    if request.method == 'POST':
        formset = Pictureformset(request.POST, request.FILES)
        form = DonationForm(request.POST)
        if formset.is_valid():
            # formset.save()
            print('Form is valid')
            # do something.
    else:
        formset = Pictureformset()
        form = DonationForm()
    return render(request, 'donations/register_donations.html', {
        'DonationForm': form,
        'formset': formset
    }) 

def register(request):
    return redirect('register_donations')