from datetime import datetime

from django import forms
from django.forms import ImageField, ModelForm, Textarea
from django.forms.models import ModelForm
from django.forms.widgets import DateInput, NumberInput, TextInput, Select
from django.utils.translation import gettext_lazy as _

from donations.models import *
from donations.models import Feedback
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
            'name': TextInput(attrs={'class':'form-control'}),
            'dtype': Select(attrs={'class':'form-control'}),
            'condition': NumberInput(attrs={'class':'form-control'}),
            'quantity': NumberInput(attrs={'class':'form-control'}),
            'desc': Textarea(attrs={'cols': 40, 'rows': 5 ,'class':'form-control'}),
        }

class CreateProjectForm(ModelForm):
    expire_date = forms.DateField(label='วันสิ้นสุดการรับ', widget=forms.DateTimeInput(attrs={'class':'form-control', 'type':'date'}),
        validators=[validate_past_date]
    )
    requiretype = forms.ModelMultipleChoiceField(label='สิ่งที่เปิดรับ',
                       widget = forms.CheckboxSelectMultiple(attrs={'class':'form-check-control'}),
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
        }
        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'propose': TextInput(attrs={'class':'form-control'}),
            'helping_people': NumberInput(attrs={'class':'form-control'}),
            'address': Textarea(attrs={'cols': 40, 'rows': 5 , 'class':'form-control'}),
            'desc': Textarea(attrs={'cols': 40, 'rows': 5 , 'class':'form-control'}),
        }

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ['album', 'sender', 'sent_date', 'donation', 'location']
        labels = {
            'header': _('หัวเรื่อง'),
            'detail': _('เนื้อความ')
        }
        widgets = {
            'header': TextInput(attrs={'class':'form-control'}),
            'detail': Textarea(attrs={'cols': 40, 'rows': 5 ,'class':'form-control'}),
        }
