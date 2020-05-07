
from .models import Feedback, Location, Donation, Album, Picture
from rest_framework import serializers

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
