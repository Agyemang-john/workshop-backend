from django.contrib import admin
from .models import *
from import_export.admin import ExportMixin
from import_export import resources

from import_export.fields import Field
from import_export.widgets import JSONWidget

from import_export.fields import Field
from import_export.resources import ModelResource

from import_export.resources import ModelResource, Field
from .models import Registration, CustomField

class RegistrationResource(ModelResource):
    class Meta:
        model = Registration
        fields = ("id", "name", "email", "workshop", "created_at")

    def __init__(self, workshop_id=None, **kwargs):
        """Dynamically add response fields based on searched workshop"""
        super().__init__()

        if workshop_id:
            response_fields = list(
                CustomField.objects.filter(workshop_id=workshop_id)
                .values_list("label", flat=True)
            )
        else:
            response_fields = list(CustomField.objects.values_list("label", flat=True))

        for field_label in response_fields:
            field_name = field_label.lower().replace(" ", "_")  # Ensure valid field names
            self.fields[field_name] = Field(attribute=None, column_name=field_label)

            # Dynamically create a method to fill the column
            setattr(self, f"dehydrate_{field_name}", self.make_dehydrate_method(field_label))

    def make_dehydrate_method(self, field_label):
        """Returns a function that fetches response for a given field_label"""
        def dehydrate_field(obj):
            response = obj.responses.filter(field__label=field_label).first()
            return response.response_text or response.response_file if response else ""
        return dehydrate_field


class CustomFieldInline(admin.TabularInline):
    model = CustomField
    extra = 1

class WorkshopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "date", "user", "status")
    inlines = [CustomFieldInline]  # Allows adding fields inside the workshop

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers and staff see everything
        return qs.filter(user=request.user)



class RegistrationResponseInline(admin.TabularInline):
    model = RegistrationResponse
    extra = 0  # Show all responses per registration

class RegistrationAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("name", "email", "workshop", "created_at")
    search_fields = ["name", "email", "workshop__title"]
    inlines = [RegistrationResponseInline]
    resource_class = RegistrationResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers and staff see everything
        return qs.filter(workshop__user=request.user)

admin.site.register(Speaker)
admin.site.register(Category)
admin.site.register(Subscribers)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Registration, RegistrationAdmin)