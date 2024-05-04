from django.urls import path
from purchase_order import views

urlpatterns = [
    path('', views.PurchaseOrderAPIView.as_view(), name="purchase_order"),
    path('<po_id>/', views.PurchaseOrderDetailAPIView.as_view(), name="purchase_order"),
    path('<po_id>/acknowledge/', views.PurchaseOrderAcknowledgeAPIView.as_view(), name="acknowledge")
]
