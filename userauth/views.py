from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.utils import timezone
from rest_framework.permissions import AllowAny


# Create your views here.
class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        
        # Validate and save user data
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # Get the actual user instance after saving
            
            return Response({
                'data': serializer.data,
                'message': f"Hi {user.first_name}, thanks for signing up. Check your email for the OTP."
            }, status=status.HTTP_201_CREATED)

        # Return validation errors if serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)