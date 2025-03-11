from django.urls import path
from .views import WorkshopListView, WorkshopDetailView, RegistrationView

urlpatterns = [
    path('workshops/', WorkshopListView.as_view(), name='workshops-list'),
    path('workshops/<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('register/', RegistrationView.as_view(), name='workshop-register'),
]