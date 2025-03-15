from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('role', 'is_active', 'is_staff')

    def has_module_permission(self, request):
        """Restrict non-superusers from seeing the User model in the admin."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Only superusers can view users."""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Only superusers can add new users."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only superusers can edit user details."""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete users."""
        return request.user.is_superuser

# Unregister the default Group model (optional, if you don’t want non-superusers to manage groups)
admin.site.unregister(Group)

# Register UserAdmin with restrictions
admin.site.register(User, UserAdmin)

admin.site.site_header = "Forms Inc."
admin.site.site_title = "Admin Dashboard"
admin.site.index_title = "Welcome to the Admin Dashboard"
