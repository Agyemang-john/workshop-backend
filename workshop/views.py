from rest_framework import generics
from .models import Workshop, Registration
from workshop.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .serializers import WorkshopSerializer

class WorkshopSearchView(APIView, PageNumberPagination):
    page_size = 10  # Define page size

    def get(self, request):
        query = request.query_params.get("q", "")
        
        workshops = Workshop.objects.filter(status="published")

        if query:
            workshops = workshops.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        paginated_workshops = self.paginate_queryset(workshops, request, view=self)
        serializer = WorkshopSerializer(paginated_workshops, many=True)
        return self.get_paginated_response(serializer.data)
    

class SubscribeAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if Subscribers.objects.filter(email=email).exists():
            return Response({"error": "You are already subscribed!"}, status=status.HTTP_400_BAD_REQUEST)

        # Save new subscription
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Subscription successful!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkshopListView(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer

class WorkshopDetailView(generics.RetrieveAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    lookup_field = 'slug'

class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

class WorkshopFieldsView(generics.ListAPIView):
    serializer_class = CustomFieldSerializer

    def get_queryset(self):
        """Fetch custom fields for a specific workshop"""
        workshop_id = self.kwargs["workshop_id"]
        return CustomField.objects.filter(workshop_id=workshop_id)

# class RegisterAttendeeView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#     def post(self, request, workshop_id):
#         """Handle attendee registration with responses"""
#         workshop = get_object_or_404(Workshop, id=workshop_id)
#         data = request.data.copy()
#         data["workshop"] = workshop.id
#         print(data)
#         serializer = FullRegistrationSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
import json

class RegisterAttendeeView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, workshop_id):
        """Handle attendee registration with responses"""
        workshop = get_object_or_404(Workshop, id=workshop_id)

        # Extract JSON Data (convert from string if needed)
        json_data = request.data.get("json_data")
        if json_data:
            try:
                json_data = json.loads(json_data)  # Convert JSON string to Python dict
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure required fields exist
        if not json_data.get("name") or not json_data.get("email"):
            return Response({"error": "Name and email are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for serializer
        data = json_data
        data["workshop"] = workshop.id  # Attach workshop ID

        # Handle file uploads
        responses = data.get("responses", [])
        for response in responses:
            field_id = response.get("field")
            file_key = f"responses[{field_id}][response_file]"
            if file_key in request.FILES:  # Check if file is uploaded for this field
                response["response_file"] = request.FILES[file_key]

        # Serialize & Save
        serializer = FullRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


