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
            'desc': Textarea(attrs={'cols': 40, 'rows': 5 }),
        }

class CreateProjectForm(ModelForm):
    expire_date = forms.DateField(
        validators=[validate_past_date]
    )
    requiretype = forms.ModelMultipleChoiceField(
                       widget = forms.CheckboxSelectMultiple,
                       queryset = RequireType.objects.all()
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
