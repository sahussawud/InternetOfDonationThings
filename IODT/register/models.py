

from django.db import models
from django.forms import ModelForm


# Create your models here.

class thing(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    is_accept = models.BooleanField(default=True)
    picture = models.ImageField()
    timestamp = models.DateTimeField(auto_now=True)
    reciever = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class thingForm(ModelForm):
    class Meta:
        model = thing
        fields = ['name', 'address', 'picture', 'reciever']

