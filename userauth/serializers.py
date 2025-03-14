from .models import User
import re
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password']
    
    def validate(self, attrs):
        password = attrs.get('password')
        
        # Custom password rules
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        # Additional Django password validation (optional)
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        # Check for duplicate email or phone number
        email = attrs.get('email')
        phone = attrs.get('phone')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email already exists. Login or reset password")
        
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("An account with this phone number already exists. Login or reset password")
        
        return super().validate(attrs)

    def create(self, validated_data):
        # Create user and hash the password
        user = User.objects.create_user(**validated_data)
        return user