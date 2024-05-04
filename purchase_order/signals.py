from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase_order.models import PurchaseOrder
from vendors.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import F, Avg

def calculate_on_time_delivery_rate(vendor) -> None:

    total_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code, 
        status="completed"
    ).count()
    
    on_time_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code,
        status='completed',
        acknowledgment_date__lte = F('delivery_date')
    ).count()

    if total_completed_orders_count > 0:
        on_time_delivery_rate = round((on_time_completed_orders_count / 
                                       total_completed_orders_count * 100)
                                , 2)
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

def calculate_quality_rating_average(vendor) -> None:
    
    completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code, 
        status="completed",
        quality_rating__isnull=False
    )

    if completed_orders_count :
        avg_quality_rating = round(completed_orders_count.aggregate(Avg('quality_rating'))['quality_rating__avg'], 2)
        vendor.quality_rating_avg = avg_quality_rating
        vendor.save()

def calculate_average_response_time(vendor) -> None:
    
    acknowledged_orders = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code, 
        status="completed",
        acknowledgment_date__isnull=False
    )
    time_differences = acknowledged_orders.annotate(
        response_time=F('acknowledgment_date') - F('issue_date')
    )
    calc_average_response_time = time_differences.aggregate(
        avg_response_time=Avg('response_time'))['avg_response_time']
    avg_response_time_in_hours =  round((calc_average_response_time.total_seconds() / 3600), 2)

    if calc_average_response_time :
        vendor.average_response_time = avg_response_time_in_hours 
        vendor.save()

def calculate_fulfillment_rate(vendor) -> None:
    # Count the number of successfully fulfilled purchase orders
    fulfilled_orders_count = PurchaseOrder.objects.filter(
        vendor=vendor.vendor_code,
        status='completed',
        quality_rating__isnull=False  # Assuming quality_rating being present indicates successful fulfillment
    ).count()

    # Count the total number of purchase orders issued to the vendor
    total_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code
    ).count()

    # Calculate the fulfillment rate
    if total_orders_count > 0:
        calc_fulfillment_rate = fulfilled_orders_count / total_orders_count * 100
        vendor.fulfillment_rate = calc_fulfillment_rate 
        vendor.save()   


@receiver(post_save, sender=PurchaseOrder)
def update_perf_matrics(sender, instance, created, **kwargs) -> None:
    order_status = instance.status.lower()
    vendor = get_object_or_404(Vendor, vendor_code = instance.vendor.vendor_code)
    
    if not created and order_status == "completed":
        # Calculate On-Time Delivery Rate
        calculate_on_time_delivery_rate(vendor)

        # Calculate Fulfillment Rate
        calculate_fulfillment_rate(vendor)

        if instance.quality_rating is not None:
            # Calculate Quality Rating Average
            calculate_quality_rating_average(vendor)

            # Calculate Average Response Time
            calculate_average_response_time(vendor)
