from django.urls import path
from vendors import views

urlpatterns = [
    path('', views.VendorsAPIView.as_view(), name="vendor"),
    path('<vendor_id>/', views.VendorProfileAPIView.as_view(), name="vendor_profile"),
    path('<vendor_id>/performance', views.VendorPerformanceAPIView.as_view(), name="vendor_profile"),
]