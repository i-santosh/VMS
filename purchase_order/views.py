from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import (PurchaseOrderSerializer, 
                          PurchaseOrderDetailSerializer, 
                          PurchaseOrderUpdateSerializer,
                          PurchaseOrderAcknowledgeSerializer)

class PurchaseOrderAPIView(APIView):
    """
    API View for Purchase Order operations.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Create a purchase order.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        List all purchase orders with an option to filter by vendor.
        """
        vendor_code = request.query_params.get('vendor_code')
        if vendor_code:
            purchase_orders = PurchaseOrder.objects.filter(
                                vendor__vendor_code__iexact=vendor_code)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class PurchaseOrderDetailAPIView(APIView):
    """
    API View for Purchase Order Details.
    """
    permission_classes = [IsAdminUser]

    def get_purchase_order(self, po_id):
        try:
            return PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound("Purchase order not found")

    def get(self, request, po_id):
        """
        Retrieve details of a specific purchase order.
        """
        purchase_order = self.get_purchase_order(po_id)
        serializer = PurchaseOrderDetailSerializer(purchase_order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, po_id):
        """
        Update a purchase order.
        """
        purchase_order = self.get_purchase_order(po_id)
        serializer = PurchaseOrderUpdateSerializer(instance=purchase_order, 
                                                   data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, po_id):
        """
        Delete a purchase order.
        """
        purchase_order = self.get_purchase_order(po_id)
        purchase_order.delete()
        return Response({"message" : "Vendor deleted"}, 
                        status=status.HTTP_204_NO_CONTENT)
    
class PurchaseOrderAcknowledgeAPIView(APIView):
    """
    API View for Purchase Order Acknowledge.
    """

    def get_purchase_order(self, po_id):
        try:
            return PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound("Purchase order not found")
        
    def post(self, request, po_id):
        """
        Acknowledge a specific purchase order.
        """
        purchase_order = self.get_purchase_order(po_id)
        serializer = PurchaseOrderAcknowledgeSerializer(purchase_order, 
                                                        data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
