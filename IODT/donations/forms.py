from django.forms import ImageField, ModelForm, Textarea
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

  
from datetime import datetime
from donations.models import *
from donations.widgets import AdvancedFileInput

def validate_past_date(value):
    if value < datetime.now().date():
        raise forms.ValidationError(
                'วันที่เลือกต้องเป็นวันหลังวันปัจจุบัน'
            )

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'dtype', 'condition', 'desc', 'quantity']

        labels = {
            'name': _('ชื่อสิ่งของบริจาค'),
            'dtype': _('ประเภท'),
            'condition': _('สภาพ'),
            'desc': _('คำอธิบายเกี่ยวกับสิ่งของบริจาค'),
            'quantity': _('จำนวน'),
        }
        widgets = {
            'desc': Textarea(attrs={'cols': 40, 'rows': 5   }),
        }

class CreateProjectForm(ModelForm):
    expire_date = forms.DateField(
        validators=[validate_past_date]
        )

    class Meta:
        model = Project
        exclude = ('recipient','location','status','album')
        labels = {
            'name': _('ชื่อโครงการ'),
            'desc': _('รายละเอียดโครงการ'),
            'requiretype': _('การบริจาคที่รองรับ'),
            'propose': _('จุดประสงค์โครงการ'),
            'helping_people': _('จำนวนคนที่จะได้รับการช่วยเหลือ'),
            'address': _('ที่อยู่ของผู้จะได้รับบริจาค'),
            'expire_date': _('วันสิ้นสุดการรับการบริจาค')
        }
        widgets = {
            'desc': Textarea(attrs={'cols': 40, 'rows': 5  }),
        }

    # Representing the many to many related field in Pizza
    requiretype = forms.ModelMultipleChoiceField(queryset=RequireType.objects.all())

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('RequireType'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.                
            initial = kwargs.setdefault('RequireType', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['RequireType'] = [t.pk for t in kwargs['RequireType'].RequireType_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field    
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.RequireType_set.clear()
           instance.RequireType_set.add(*self.cleaned_data['RequireType'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance