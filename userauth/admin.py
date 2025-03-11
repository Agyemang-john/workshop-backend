from django.contrib import admin
from .models import *

admin.site.register(User)


admin.site.site_header = "Forms Inc."
admin.site.site_title = "Admin Dashboard"
admin.site.index_title = "Welcome to the Admin Dashboard"
