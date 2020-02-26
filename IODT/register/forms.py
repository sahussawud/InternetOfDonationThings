

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

class RegThingForm(forms.ModelForm):
    class Meta:
        model = thing
        fields= ["name", "address", "is_accept", "picture", "reciever",]
