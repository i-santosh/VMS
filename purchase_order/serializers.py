from rest_framework.serializers import ModelSerializer
from .models import PurchaseOrder

class PurchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["po_number", "vendor", "order_date", "delivery_date", "items", "quantity", "status", "issue_date", "acknowledgment_date"]

class PurchaseOrderDetailSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        
class PurchaseOrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["status", "quality_rating", "acknowledgment_date"]
        
class PurchaseOrderAcknowledgeSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["acknowledgment_date"]