from rest_framework.serializers import ModelSerializer
from .models import Vendor

class VendorSerializer(ModelSerializer):
    """
    Vendor Basic
    """
    class Meta:
        model = Vendor
        fields = ["name", "vendor_code", "contact_details", "address"]
        

class VendorProfileSerializer(ModelSerializer):
    """
    Vendor Profile
    """
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorUpdateSerializer(ModelSerializer):
    """
    Vendor Update
    """
    class Meta:
        model = Vendor
        fields = ["name","contact_details", "address"]

class VendorPerformanceSerializer(ModelSerializer):
    """
    Vendor performance
    """
    class Meta:
        model = Vendor
        fields = ["name", "on_time_delivery_rate", 
                  "quality_rating_avg", 
                  "average_response_time",
                  "fulfillment_rate"]
