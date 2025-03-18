from django.db import models
from django.utils.text import slugify
from userauth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    profile_image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Workshop(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    STATUS = (
        ("draft", "Draft"),
        ("disabled", "Disabled"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="workshops")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workshops")
    speaker = models.ManyToManyField(Speaker,  related_name="workshops")
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255, choices=[('online', 'Online'), ('venue', 'Venue')])
    venue_address = models.CharField(max_length=255, blank=True, null=True)  # If physical
    google_map_link = models.URLField(blank=True, null=True)  # If physical
    google_meet_link = models.URLField(blank=True, null=True)  # If online
    google_meet_password = models.CharField(max_length=50, blank=True, null=True)  # If online
    cover_image = CloudinaryField('image', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager() # Custom Manager

    class Meta:
        ordering = ('-created_at',)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Workshop, self).save(*args, **kwargs)
    
    @property
    def workshop_status(self):
        """Dynamically determine the workshop status based on time"""
        if self.date > now():
            return "Upcoming"
        elif self.date <= now() and now() <= (self.date + self.duration):
            return "Ongoing"
        else:
            return "Completed"
    
    def clean(self):
        """
        Validate that the correct location details are provided.
        """
        if self.location == 'online' and not self.google_meet_link:
            raise ValidationError("Google Meet link must be provided for online workshops.")

        if self.location == 'venue' and (not self.venue_address or not self.google_map_link):
            raise ValidationError("Venue address and Google Map link must be provided for physical workshops.")




class Subscribers(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}"

    
class CustomField(models.Model):
    FIELD_TYPES = [
        ("text", "Text"),
        ("email", "Email"),
        ("multiline", "Multiline"),
        ("number", "Number"),
        ("file", "File Upload"),
        ("checkbox", "Checkbox"),
        ("select", "Dropdown"),
        ("multi_select", "Multiple Dropdown"),
        ("radio", "Radio"),
    ]

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="custom_fields")
    label = models.CharField(max_length=255)  # Question text (e.g., "Your department?")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)  # Field type
    required = models.BooleanField(default=True)  # Is this field required?
    options = models.JSONField(blank=True, null=True)  # For dropdown (e.g., {"choices": ["Option1", "Option2"]})

    def __str__(self):
        return f"{self.workshop.title} - {self.label}"

class Registration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=255)  # Attendee Name
    email = models.EmailField()  # Attendee Email
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    class Meta:
        unique_together = ("workshop", "email")

    def __str__(self):
        return f"{self.name} - {self.workshop.title}"

class RegistrationResponse(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="responses")
    field = models.ForeignKey(CustomField, on_delete=models.CASCADE)  # Field being answered
    response_text = models.TextField(blank=True, null=True)  # Stores text, email, number responses
    response_file = CloudinaryField('image', null=True, blank=True)  # Stores file uploads

    def __str__(self):
        return f"{self.registration.name} - {self.field.label}"