from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vendor
from .serializers import (VendorSerializer,
                        VendorProfileSerializer,
                        VendorUpdateSerializer)

class VendorsAPIView(APIView):

    # List all vendors 
    def get(self, request):
        all_vendors = Vendor.objects.all()
        serializer = VendorSerializer(all_vendors, many=True)
        return Response(serializer.data)
    
    # Create a new vendor
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorProfileAPIView(APIView):

    # Retrieve a specific vendor's details 
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
        serializer = VendorProfileSerializer(vendor)
        return Response(serializer.data)

    # Update a vendor's details 
    def put(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, vendor_code = vendor_id)
        serializer = VendorUpdateSerializer(instance=vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a vendor
    def delete(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, vendor_code = vendor_id)
        vendor.delete()
        return Response({"message" : "Vendor deleted"}, status=status.HTTP_204_NO_CONTENT)     
        