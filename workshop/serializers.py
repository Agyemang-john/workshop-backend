from rest_framework import serializers
from .models import *
from django.conf import settings


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = ["id", "email"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Speaker
        fields = '__all__'
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/{obj.profile_image}"
        return None

    
class WorkshopSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    workshop_status = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = '__all__'
    
    def get_workshop_status(self, obj):
        return obj.workshop_status
    
    def get_cover_image(self, obj):
        if obj.cover_image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/{obj.cover_image}"
        return None

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class SubscribersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = '__all__'
# Compare this snippet from workshop/views.py:
# from rest_framework import viewsets

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ["id", "workshop", "label", "field_type", "required", "options"]

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["id", "workshop", "name", "email", "created_at"]
    
    def validate(self, data):
        """Ensure a user does not register multiple times for the same workshop."""
        workshop = data["workshop"]
        email = data["email"]

        if Registration.objects.filter(workshop=workshop, email=email).exists():
            raise serializers.ValidationError("You have already registered for this workshop.")

        return data


import json
class RegistrationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationResponse
        fields = ["id", "field", "response_text", "response_file"]

    def to_internal_value(self, data):
        """Convert response_text lists to JSON strings before validation."""
        if isinstance(data.get("response_text"), list):
            data["response_text"] = json.dumps(data["response_text"])  # Convert list to JSON string
        
        return super().to_internal_value(data)

    def validate_response_text(self, value):
        """Ensure response_text is a string (after conversion)"""
        if not isinstance(value, str):
            raise serializers.ValidationError("Response must be a string.")
        return value

# class FullRegistrationSerializer(serializers.ModelSerializer):
#     responses = RegistrationResponseSerializer(many=True)

#     class Meta:
#         model = Registration
#         fields = ["id", "workshop", "name", "email", "responses"]
    
#     def validate_response_file(self, value):
#         if value and not hasattr(value, "file"):
#             raise serializers.ValidationError("Invalid file. Please upload a valid file.")
#         return value

#     def create(self, validated_data):
#         responses_data = validated_data.pop("responses")  # Extract responses from data
#         registration = Registration.objects.create(**validated_data)  # Create Registration

#         # ✅ Assign `registration` to each response before saving
#         for response_data in responses_data:
#             RegistrationResponse.objects.create(
#                 registration=registration,  # Manually attach registration
#                 **response_data
#             )

#         return registration

class FullRegistrationSerializer(serializers.ModelSerializer):
    responses = RegistrationResponseSerializer(many=True)

    class Meta:
        model = Registration
        fields = ["id", "workshop", "name", "email", "responses"]

    def create(self, validated_data):
        responses_data = validated_data.pop("responses")  # Extract responses
        registration = Registration.objects.create(**validated_data)  # Create Registration

        # Convert all `response_text` values to strings before saving
        for response_data in responses_data:
            if isinstance(response_data.get("response_text"), list):
                response_data["response_text"] = json.dumps(response_data["response_text"])

            RegistrationResponse.objects.create(
                registration=registration,
                **response_data
            )

        return registration






