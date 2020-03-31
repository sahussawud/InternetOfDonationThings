from django.forms import ModelForm, Textarea
from donations.models import *
from django.utils.translation import gettext_lazy as _

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['name', '_type', 'condition', 'desc', 'quantity']

        labels = {
            'name': _('ชื่อสิ่งของบริจาค'),
            '_type': _('ประเภท'),
            'condition': _('สภาพ'),
            'desc': _('คำอธิบายเกี่ยวกับสิ่งของบริจาค'),
            'quantity': _('จำนวน'),
        }
        widgets = {
            'desc': Textarea(attrs={'cols': 40, 'rows': 5   }),
        }

# class PhotoForm(ModelForm):
#     class Meta:
#         model = Picture
#         fields = ['url']
#         labels = {
#             'url': _('เพิ่มรูปภาพ'),
#         }
 