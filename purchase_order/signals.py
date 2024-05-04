from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase_order.models import PurchaseOrder
from vendors.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import F, Avg

def calculate_on_time_delivery_rate(vendor_code) -> None:

    total_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor_code, 
        status="completed"
    ).count()
    
    on_time_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor_code,
        status='completed',
        acknowledgment_date__lte = F('delivery_date')
    ).count()

    if total_completed_orders_count > 0:
        vendor = get_object_or_404(Vendor, vendor_code = vendor_code)
        on_time_delivery_rate = round((on_time_completed_orders_count / 
                                       total_completed_orders_count * 100)
                                , 2)
        
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

def calculate_quality_rating_average(vendor_code) -> None:
    
    completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor_code, 
        status="completed",
        quality_rating__isnull=False
    )

    if completed_orders_count :
        avg_quality_rating = round(completed_orders_count.aggregate(Avg('quality_rating'))['quality_rating__avg'], 2)
        print("avg_quality_rating: ", avg_quality_rating)
        vendor = get_object_or_404(Vendor, vendor_code = vendor_code)
        
        vendor.quality_rating_avg = avg_quality_rating
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_perf_matrics(sender, instance, created, **kwargs) -> None:
    order_status = instance.status.lower()
    vendor_code = instance.vendor.vendor_code
    
    if not created and order_status == "completed":
        
        # Calculate On-Time Delivery Rate
        calculate_on_time_delivery_rate(vendor_code)

        # Calculate Quality Rating Average
        if instance.quality_rating is not None:
            calculate_quality_rating_average(vendor_code)
