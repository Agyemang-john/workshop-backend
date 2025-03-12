from django.db import models
from django.utils.text import slugify
from userauth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError


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
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255, choices=[('online', 'Online'), ('venue', 'Venue')])
    views = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    venue_address = models.CharField(max_length=255, blank=True, null=True)  # If physical
    google_map_link = models.URLField(blank=True, null=True)  # If physical
    google_meet_link = models.URLField(blank=True, null=True)  # If online
    google_meet_password = models.CharField(max_length=50, blank=True, null=True)  # If online
    cover_image = models.ImageField(upload_to='workshop_images/')
    status = models.CharField(max_length=50, choices=STATUS, default='in_review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager() # Custom Manager


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

class Speaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='speakers/')
    workshop = models.ManyToManyField(Workshop, related_name='speakers')

    def __str__(self):
        return self.name

class Registration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=255)
    level = models.CharField(max_length=20)
    expectations = models.TextField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.workshop.title}"


class Subscribers(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"



