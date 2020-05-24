
from pkg_resources import require

from rest_framework import serializers

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

from django.db.models import Sum
class ProjectOverviewSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    album = AlbumSerializer()
    current_helping = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'propose', 'requiretype', 'expire_date', 'recipient', 'location', 'album', 'helping_people', 'current_helping']
        read_only_fields = ['id', 'name', 'propose', 'requiretype', 'expire_date', 'recipient', 'location', 'album', 'helping_people', 'current_helping']
    def get_current_helping(self, obj):
            quantity = Donation.objects.filter(project=obj).aggregate(Sum('quantity'))
            return quantity