from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, email_or_phone=None, password=None, **kwargs):
        try:
            data = email_or_phone
            user = User.objects.get(Q(email=data) | Q(phone=data))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None