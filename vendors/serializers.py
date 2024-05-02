from rest_framework.serializers import ModelSerializer
from .models import Vendor

class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name", "contact_details", "vendor_code"]

class VendorProfileSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['id']