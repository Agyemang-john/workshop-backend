from celery import shared_task
from django.utils.timezone import now, localtime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta
from .models import Workshop, Registration


@shared_task
def send_workshop_reminder_emails():
    """Send reminder emails to attendees a day before the workshop."""
    tomorrow = localtime(now()).date() + timedelta(days=1)
    
    workshops = Workshop.objects.filter(date__date=tomorrow, status='published')

    for workshop in workshops:
        attendees = workshop.registrations.all()
        
        for attendee in attendees:
            subject = f"Reminder: {workshop.title} is happening tomorrow!"
            
            # Render HTML email template
            html_content = render_to_string("workshop_reminder.html", {
                "attendee_name": attendee.name,
                "workshop_title": workshop.title,
                "workshop_date": workshop.date.strftime('%A, %d %B %Y'),
                "workshop_time": workshop.date.strftime('%I:%M %p'),
                "workshop_location": "Online" if workshop.location == "online" else workshop.venue_address,
                "google_meet_link": workshop.google_meet_link if workshop.location == "online" else "#",
                "venue_address": workshop.venue_address or "N/A",
                "google_map_link": workshop.google_map_link or "#",
            })
            
            text_content = strip_tags(html_content)  # Plain text version

            email = EmailMultiAlternatives(subject, text_content, 'noreply@yourdomain.com', [attendee.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

    return f"Sent {sum(workshops.count())} workshop reminders."
