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

        # ✅ Fetch only fields for the specific workshop
        if workshop_id:
            response_fields = list(
                CustomField.objects.filter(workshop_id=workshop_id)
                .values_list("label", flat=True)
            )
        else:
            # ⚠ Fallback: Fetch all fields (for debugging, remove later)
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


# class RegistrationResource(ModelResource):
#     class Meta:
#         model = Registration
#         fields = ("id", "name", "email", "workshop", "created_at")

#     def __init__(self):
#         """Dynamically add response fields as columns"""
#         super().__init__()
#         response_fields = list(CustomField.objects.values_list("label", flat=True))  # Get all field labels

#         for field_label in response_fields:
#             field_name = field_label.lower().replace(" ", "_")  # Ensure valid field names
#             self.fields[field_name] = Field(attribute=None, column_name=field_label)

#             # Dynamically create a method to fill the column
#             setattr(self, f"dehydrate_{field_name}", self.make_dehydrate_method(field_label))

#     def make_dehydrate_method(self, field_label):
#         """Returns a function that fetches response for a given field_label"""
#         def dehydrate_field(obj):
#             response = obj.responses.filter(field__label=field_label).first()
#             return response.response_text or response.response_file if response else ""
#         return dehydrate_field




class CustomFieldInline(admin.TabularInline):
    model = CustomField
    extra = 1

class WorkshopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "date")
    inlines = [CustomFieldInline]  # Allows adding fields inside the workshop

class RegistrationResponseInline(admin.TabularInline):
    model = RegistrationResponse
    extra = 0  # Show all responses per registration

class RegistrationAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("name", "email", "workshop", "created_at")
    search_fields = ["name", "email", "workshop__title"]
    inlines = [RegistrationResponseInline]
    resource_class = RegistrationResource 

# class RegistrationAdmin(ExportMixin, admin.ModelAdmin):
#     list_display = ("name", "email", "workshop", "created_at")
#     search_fields = ["name", "email", "workshop__title"]
#     inlines = []

#     def get_export_queryset(self, request):
#         """Override to dynamically determine the workshop ID"""
#         queryset = super().get_export_queryset(request)
        
#         # ✅ Extract workshop ID correctly
#         workshop_id = request.GET.get("q")  # Get workshop title from search query
        
#         if workshop_id:
#             # Get actual ID from the Workshop model (if needed)
#             from .models import Workshop  
#             workshop = Workshop.objects.filter(title__icontains=workshop_id).first()
#             if workshop:
#                 workshop_id = workshop.id
#             else:
#                 workshop_id = None
        
#         # ✅ Pass the correct workshop ID to the resource
#         self.resource_class = lambda: RegistrationResource(workshop_id=workshop_id)
#         return queryset


admin.site.register(Speaker)
admin.site.register(Category)
admin.site.register(Subscribers)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Registration, RegistrationAdmin)