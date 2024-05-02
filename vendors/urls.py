from django.urls import path
from .views import VendorsAPIView, VendorProfileAPIView

urlpatterns = [
    path('', VendorsAPIView.as_view(), name="vendor"),
    path('<vendor_id>/', VendorProfileAPIView.as_view(), name="vendor_profile"),
]