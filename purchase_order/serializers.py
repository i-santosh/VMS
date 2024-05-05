from rest_framework.serializers import ModelSerializer
from .models import PurchaseOrder

class PurchaseOrderSerializer(ModelSerializer):
    """
    Purchase Order Basic
    """
    class Meta:
        model = PurchaseOrder
        fields = ["po_number", "vendor", "order_date", "delivery_date", "items", "quantity", "status", "issue_date", "acknowledgment_date"]

class PurchaseOrderDetailSerializer(ModelSerializer):
    """
    Purchase Order Detail
    """
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        
class PurchaseOrderUpdateSerializer(ModelSerializer):
    """
    Purchase Order Update
    """
    class Meta:
        model = PurchaseOrder
        fields = ["status", "quality_rating"]
        
class PurchaseOrderAcknowledgeSerializer(ModelSerializer):
    """
    Purchase Order Acknowledge
    """
    class Meta:
        model = PurchaseOrder
        fields = ["acknowledgment_date"]