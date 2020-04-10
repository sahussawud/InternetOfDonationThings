

from email.policy import default

# Create your models here.
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey

from datetime import datetime 
from register.models import Doner, Recipient


# from management.models import ClassRoom, Student
class Location(models.Model):
    TYPES = (
        ('feedback', 'การตอบกลับ'),
        ('shipping', 'การขนส่ง'),
        ('update', 'การอัปเดต')
    )
    name = models.CharField(max_length=40)
    _type = models.CharField(max_length=10,choices=TYPES)
    ladtitude = models.CharField(max_length=50)
    longtitude = models.CharField(max_length=50)
class RequireType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    name = models.CharField(max_length=30,blank=True)
    desc = models.CharField(max_length=255,blank=True)

class Project(models.Model):
    STATUS = (
        ('open','เปิดรับริจาค'),
        ('close', 'ปิดรับบริจาค'),
        ('process', 'ดำเนินการ'),
        ('finished', 'เสร็จสิ้น')
    )
    name = models.CharField(max_length=50)
    desc = models.TextField()
    requiretype = models.ManyToManyField(RequireType)
    propose = models.CharField(max_length=255)
    helping_people = models.SmallIntegerField()
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    create_date = models.DateField(auto_now_add=True)
    expire_date = models.DateTimeField()
    recipient = models.ForeignKey(Recipient,on_delete=models.SET_NULL, null=True)
    album = models.OneToOneField(Album, on_delete=models.CASCADE, null=True)

    # def amount_donation(self):

class Picture(models.Model):
    name = models.CharField(max_length=30, blank=True)
    url = models.ImageField(upload_to='album/pic/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=0)

class Donation(models.Model):
    STATUS = (
        ('Yet', 'ยังไม่บริจาค'),
        ('Pending','รอการยืนยัน'),
        ('Recieve','ได้รับของบริจาค')
    )
    # TYPE = (
    #     ('MED', 'อุปกรณ์ทางการเเพทย์'),
    #     ('GARMENT', 'เครื่องนุ่งห่ม'),
    #     ('CONSUMABLE', 'โภคภัณฑ์'),
    #     ('CAPITAL','เงิน'),
    #     ('SPORT EQUIPMENT', 'อุปกรณ์กีฬา'),
    #     ('RECREATION','อุปกรณ์สันทนาการ'),
    #     ('COMPUTER', 'คอมพิวเตอร์เเละอุปกรณ์'),
    #     ('MUSIC','เครื่องดนตรี'),
    #     ('TEACH', 'อุปกรณ์ครุภัณฑ์')
    # )
    CONDITION = (
        ('1','ชำรุด'),
        ('2','ต้องซ่อม'),
        ('3','ดี'),
        ('4','เสมือนใหม่'),
        ('5','ใหม่'),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])
    dtype = models.ForeignKey(RequireType, null=True, on_delete=SET_NULL)
    desc = models.TextField()
    condition = models.CharField(max_length=1, choices=CONDITION)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now=True)
    donor = models.ForeignKey(Doner, on_delete=models.CASCADE, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    album = models.OneToOneField(Album, on_delete=models.CASCADE, null=True)

class Qrcode(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=255)

class SendDetail(models.Model):
    METHOD = (
        ('EMS','ส่งทางไปรษณีย์'),('SELF','ไปส่งที่ผุ้รับด้วยตัวเอง'),('TAKEHOME','ผุ้รับมารับ'),('TRANFER','โอนเงิน')
    )
    _type = models.CharField(max_length=8, choices=METHOD)

class Shipping(models.Model):
    S_COMPANY = (
        ('THAIPOST', 'ไปรษณีย์ไทย'),
        ('KERRY','เคอรรี่'),
        ('FLASH', 'เเฟลช')
    )
    tracking_id = models.CharField(max_length=50)
    company = models.CharField(choices=S_COMPANY,max_length=8)
    reciept = models.ImageField(upload_to='shipping/slip/')
    send_datetime = models.DateTimeField()
    senddetail = models.OneToOneField(SendDetail, on_delete=models.CASCADE, default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)

class Feedback(models.Model):
    sender = models.ForeignKey(Recipient, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=40)
    detail = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
