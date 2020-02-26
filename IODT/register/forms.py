

# def regForm(forms.ModalForm):
#     name = models.CharField()
#     address = models.TextField()
#     is_accept = models.BooleanField()
#     picture = models.ImageField()

#     class Meta:
#         model = thing
#         field = ('name', 'address', 'is_accept','picture')

from django import forms
from .models import thing

# class RegThingForm(forms.ModelForm):
#     class Meta:
#         model = thing
#         fields= ["name", "address", "is_accept", "picture", "reciever",]


class thingForm(forms.Form):
    name = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea, required=True)
    picture = forms.ImageField()
    reciever =  forms.CharField(max_length=50)
    

