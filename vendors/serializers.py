from rest_framework.serializers import ModelSerializer
from .models import Vendor

class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name", "vendor_code", "contact_details", "address"]
        

class VendorProfileSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['id']

class VendorUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name","contact_details", "address"]