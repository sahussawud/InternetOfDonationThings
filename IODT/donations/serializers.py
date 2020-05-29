
from django.db.models import Sum
from pkg_resources import require
from datetime import datetime, timedelta
from django.utils import timezone

from donations.models import RequireType
from rest_framework import serializers
from django.db.models import Count

from .models import Album, Donation, Feedback, Location, Picture, Project


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'url']
        read_only_fields = ['id']

class AlbumSerializer(serializers.ModelSerializer):
    picture_set = PictureSerializer(many=True, required=False)
    class Meta:
        model = Album
        fields = ['id', 'name', 'picture_set']
        read_only_fields = ['id']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'ladtitude', 'longtitude']
        read_only_fields = ['id']

class FeedbackSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    album = AlbumSerializer(required=False)
    class Meta:
        model = Feedback
        fields = ['id', 'sender', 'header', 'detail', 'sent_date', 'location', 'album']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']
        read_only_fields = ['id']

class DonationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    album = AlbumSerializer(required=False)
    project = ProjectSerializer(required=False)
    class Meta:
        model = Donation
        field = ['id', 'name', 'date', 'project', 'location', 'album']

class RequireTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequireType
        fields = ['id', 'name']

class ProjectOverviewSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    album = AlbumSerializer()
    current_helping = serializers.SerializerMethodField()
    # status = serializers.SerializerMethodField()
    requiretype = RequireTypeSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'propose', 'requiretype', 'expire_date', 'recipient', 'location', 'album', 'helping_people', 'current_helping','status']
        read_only_fields = ['id', 'name', 'propose', 'requiretype', 'expire_date', 'recipient', 'location', 'album', 'helping_people', 'current_helping','status']
    def get_current_helping(self, obj):
        quantity = Donation.objects.filter(project=obj).aggregate(Sum('quantity'))
        return quantity

    # def get_status(self, obj):
    #     status = ''
    #     print(obj.expire_date, datetime.today(), type(obj.expire_date-timezone.now()))
    #     if obj.expire_date < timezone.now():
    #         status = 'deactive'
    #     elif obj.expire_date-timezone.now() > timedelta(days=1):
    #         status = 'active'
    #     else:
    #         status = 'patial_deactive'
    #     return status

class ProjectSummarySerializer(serializers.ModelSerializer):
    status_donation = serializers.SerializerMethodField()
    expire_duration = serializers.SerializerMethodField()
    condition_count = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'expire_duration', 'status', 'status_donation', 'condition_count']
        read_only_fields = ['id', 'expire_duration', 'status_donation', 'condition_count']
    def get_status_donation(self, obj):
        item = {}
        donation = Donation.objects.filter(project=obj)
        quantity = donation.values('status').annotate(amount=Count('status'))
        for i in quantity:
            item['Pending'] = i.get('amount') if i.get('status') == 'Pending' else 0
            item['Recieve'] = i.get('amount') if i.get('status') == 'Recieve' else 0
        item['All'] = obj.helping_people
        return item

    def get_expire_duration(self, obj):
        delta = obj.expire_date-timezone.now()
        return { 'day': str(delta.days),
                 'hour':(datetime.utcfromtimestamp(0) + delta).strftime('%H'),
                 'min':(datetime.utcfromtimestamp(0) + delta).strftime('%M'),
                 'from': timezone.now()}

    def get_condition_count(self, obj):
        item = {'fix':0,'stardard':0,'good':0, 'broke':0, 'best':0}
        quantity = Donation.objects.filter(project=obj).values('condition').annotate(amount=Sum('quantity'))
        for i in quantity:
            if i.get('condition') == '1':
                item['broke'] = i.get('amount')
            if i.get('condition') == '2':
                item['fix'] = i.get('amount')
            if i.get('condition') == '3':   
                item['standard'] = i.get('amount')
            if i.get('condition') == '4': 
                item['good'] = i.get('amount')
            if i.get('condition') == '5':
                item['best'] = i.get('amount') 
        return item
