from rest_framework import serializers
from .models import Workshop, Speaker, Registration

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'

class WorkshopSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
# Compare this snippet from workshop/views.py:
# from rest_framework import viewsets