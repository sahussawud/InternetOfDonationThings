from django.forms import ModelForm, Textarea, ImageField, widgets
from donations.models import *
from django.utils.translation import gettext_lazy as _
from string import Template
from django.utils.safestring import mark_safe

class PictureWidget(widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))

class DonationForm(ModelForm):
    photo = ImageField(widget=PictureWidget)
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
 