from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase_order.models import PurchaseOrder
from vendors.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import F

def calculate_on_time_delivery_rate(purchase_order_instance) -> None:
    total_completed_orders_count = PurchaseOrder.objects.filter(
        vendor=purchase_order_instance.vendor, 
        status="completed"
    ).count()
    on_time_completed_orders_count = PurchaseOrder.objects.filter(
        vendor=purchase_order_instance.vendor,
        status='completed',
        acknowledgment_date__lte = F('delivery_date')
    ).count()

    if total_completed_orders_count > 0:
        vendor = get_object_or_404(Vendor, vendor_code = purchase_order_instance.vendor)
        on_time_delivery_rate = round((on_time_completed_orders_count / total_completed_orders_count * 100)
                                      , 2)
        print(on_time_delivery_rate)
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_perf_matrics(sender, instance, created, **kwargs) -> None:
    order_status : str = instance.status.lower()
    if not created and order_status == "completed":
        calculate_on_time_delivery_rate(instance)
