from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vendor
from rest_framework.permissions import IsAuthenticated
from .serializers import (VendorSerializer,
                          VendorProfileSerializer,
                          VendorUpdateSerializer,
                          VendorPerformanceSerializer)

class VendorsAPIView(APIView):
    """
    API View for Vendor operations.
    """

    def get(self, request):
        """
        Lists all vendors.
        """
        all_vendors = Vendor.objects.all()
        serializer = VendorSerializer(all_vendors, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        """
        Creates a new vendor with the provided data.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorProfileAPIView(APIView):
    """
    API View for specific Vendor operations.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        """
        Retrieves a specific vendor's details.
        """
        vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
        serializer = VendorProfileSerializer(vendor)
        return Response(serializer.data)

    
    def put(self, request, vendor_id):
        """
        Updates a vendor's details with the provided data.
        """ 
        vendor = get_object_or_404(Vendor, vendor_code = vendor_id)
        serializer = VendorUpdateSerializer(instance=vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, vendor_id):
        """
        Deletes a specific vendor.
        """
        vendor = get_object_or_404(Vendor, vendor_code = vendor_id)
        vendor.delete()
        return Response({"message" : "Vendor deleted"}, status=status.HTTP_204_NO_CONTENT)     

class VendorPerformanceAPIView(APIView):
    """
    API View for retrieving a specific vendor's performance.
    """ 
    def get(self, request, vendor_id):
        """
        Retrieves a specific vendor's performance.
        """
        vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)