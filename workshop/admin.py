from django.contrib import admin
from .models import *

class SpeakerAdmin(admin.ModelAdmin):  # Speaker should not be registered separately
    model = Speaker
    extra = 1

class WorkshopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    list_display = ['title', 'status']

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Speaker)
admin.site.register(Registration)
