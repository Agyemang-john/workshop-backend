# utils.py
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import pytz
from urllib.parse import urlencode


def generate_ics_file(workshop):
    cal = Calendar()
    event = Event()

    event.add('summary', workshop.title)
    event.add('description', workshop.description or 'Workshop Event')
    event.add('location', "Online" if workshop.location == "online" else workshop.venue_address)

    # Use aware datetimes
    start = make_aware(workshop.date)
    end = start + timedelta(hours=2)  # Adjust as needed
    event.add('dtstart', start)
    event.add('dtend', end)

    event.add('dtstamp', datetime.now(pytz.UTC))
    cal.add_component(event)

    return cal.to_ical()


def get_google_calendar_link(workshop):
    start = workshop.date.strftime('%Y%m%dT%H%M%SZ')
    end = (workshop.date + timedelta(hours=2)).strftime('%Y%m%dT%H%M%SZ')

    params = {
        'action': 'TEMPLATE',
        'text': workshop.title,
        'dates': f'{start}/{end}',
        'details': workshop.description or '',
        'location': 'Online' if workshop.location == 'online' else workshop.venue_address,
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)
