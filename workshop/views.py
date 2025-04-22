from rest_framework import generics
from .models import Workshop, Registration
from workshop.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .serializers import WorkshopSerializer
from .utils import generate_ics_file, get_google_calendar_link



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

import json

class RegisterAttendeeView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, workshop_id):
        """Handle attendee registration with responses"""
        workshop = get_object_or_404(Workshop, id=workshop_id)

        # Extract and validate JSON data
        json_data = request.data.get("json_data")
        if json_data:
            try:
                json_data = json.loads(json_data)  # Convert JSON string to dict
                print("🔍 Incoming JSON Data:", json_data)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure required fields exist
        required_fields = ["name", "email"]
        if any(field not in json_data for field in required_fields):
            return Response({"error": "Name and email are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Attach workshop ID
        json_data["workshop"] = workshop.id  

        # Serialize & Save
        serializer = FullRegistrationSerializer(data=json_data)
        if serializer.is_valid():
            registration = serializer.save()

            # Prepare email context
            context = {
                "name": registration.name,
                "workshop_title": workshop.title,
                "workshop_date": workshop.date.strftime("%A, %d %B %Y at %I:%M %p"),
                "location": "Online" if workshop.location == "online" else workshop.venue_address,
                "google_meet_link": workshop.google_meet_link if workshop.location == "online" else None,
                "google_map_link": workshop.google_map_link if workshop.location == "venue" else None
            }

            context["google_calendar_link"] = get_google_calendar_link(workshop)

            # Load email template
            html_content = render_to_string("registration_confirmation.html", context)
            text_content = strip_tags(html_content)  

            ics_file = generate_ics_file(workshop)

            try:
                # Send confirmation email
                email = EmailMultiAlternatives(
                    subject="🎉 Your Workshop Registration is Confirmed!",
                    body=text_content,
                    from_email="noreply@workshop.com",
                    to=[registration.email]
                )
                email.attach_alternative(html_content, "text/html")
                # 📎 Attach calendar file
                email.attach(f"{workshop.slug}.ics", ics_file, "text/calendar")
                email.send()
                return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Email Error: {e}")  # Log the error
                return Response({
                    "message": "You've registered successfully, but we couldn't send the confirmation email."
                }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

