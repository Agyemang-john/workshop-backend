from django import forms
import json
from .models import CustomForm


class CustomFormAdminForm(forms.ModelForm):
    FIELD_CHOICES = [
        ("text", "Text Field"),
        ("email", "Email Field"),
        ("number", "Number Field"),
        ("file", "File Upload"),
    ]

    json_fields = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 80}),
        required=False,
        help_text="Enter JSON in this format: {\"name\": \"text\", \"email\": \"email\"}"
    )

    def clean_json_fields(self):
        """Ensure valid JSON format"""
        data = self.cleaned_data["json_fields"]
        try:
            return json.loads(data)  # Convert string to JSON
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format. Please check the syntax.")

    class Meta:
        model = CustomForm
        fields = "__all__"
