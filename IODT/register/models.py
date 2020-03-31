


# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class User(AbstractUser):
    address = models.TextField()
    phone = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profiles/')

class Recipient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.FloatField()
    response_rate = models.FloatField()
    desc = models.TextField()

class Organization(models.Model):
    recipient = models.OneToOneField(Recipient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    establish_date = models.DateField()
    vision = models.CharField(max_length=255)

class People(models.Model):
    SEX = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    recipient = models.OneToOneField(Recipient, on_delete=models.CASCADE)
    sex = models.CharField(choices=SEX, max_length=1)


class Doner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.CharField(choices=People.SEX, max_length=1)
    donate_amount = models.FloatField()
    helping_amount = models.IntegerField()


