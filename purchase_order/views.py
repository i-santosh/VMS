from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from .serializers import (PurchaseOrderSerializer, 
                          PurchaseOrderDetailSerializer, 
                          PurchaseOrderUpdateSerializer)

class PurchaseOrderAPIView(APIView):
    # Create a purchase order
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # List all purchase orders with an option to filter by vendor
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        vendor_code = request.query_params.get('vendor_code')
        if vendor_code:
            purchase_orders = purchase_orders.filter(
                                vendor__vendor_code__iexact=vendor_code)
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class PurchaseOrderDetailAPIView(APIView):
    # Retrieve details of a specific purchase order
    def get(self, request, po_id):
        purchase_orders = get_object_or_404(PurchaseOrder, po_number=po_id)
        serializer = PurchaseOrderDetailSerializer(purchase_orders)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    # Update a purchase order
    def put(self, request, po_id):
        purchase_orders = get_object_or_404(PurchaseOrder, po_number=po_id)
        serializer = PurchaseOrderUpdateSerializer(instance=purchase_orders, 
                                                   data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a purchase order
    def delete(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, po_number=po_id)
        purchase_order.delete()
        return Response({"message" : "Vendor deleted"}, 
                        status=status.HTTP_204_NO_CONTENT)