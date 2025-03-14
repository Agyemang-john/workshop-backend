from django.urls import path
from .views import *

urlpatterns = [
    path('workshops/', WorkshopListView.as_view(), name='workshops-list'),
    path('workshop/<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('register/', RegistrationView.as_view(), name='workshop-register'),

    path("workshop/<int:workshop_id>/fields/", WorkshopFieldsView.as_view(), name="workshop-fields"),
    path("workshop/<int:workshop_id>/register/", RegisterAttendeeView.as_view(), name="workshop-register"),
]