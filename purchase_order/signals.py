from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase_order.models import PurchaseOrder
from vendors.models import Vendor, HistoricalPerformance
from django.shortcuts import get_object_or_404
from django.db.models import F, Avg
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs) -> None:
    """
    Signal for updating performance metrics in real-time.
    """
    
    if not created and instance.status.lower() == "completed":
        try:
            vendor = Vendor.objects.get(vendor_code=instance.vendor.vendor_code)
        except ObjectDoesNotExist:
            return  # Vendor not found
        
        # Calculate metrics
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        if instance.quality_rating is not None:
            quality_rating_average = calculate_quality_rating_average(vendor)
            average_response_time = calculate_average_response_time(vendor)
        else:
            quality_rating_average = None
            average_response_time = None

        """
        Add performance record to History
        """
        HistoricalPerformance.add_performance_record(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_average,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )

def calculate_on_time_delivery_rate(vendor):
    """
    Calculate on time delivery rate of a specified vendor.
    """

    total_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code, 
        status="completed"
    ).count()
    
    on_time_completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code,
        status='completed',
        acknowledgment_date__lte = F('delivery_date')
    ).count()

    # Calculating On Time delivery rate
    if total_completed_orders_count > 0:
        on_time_delivery_rate = round((on_time_completed_orders_count / 
                                       total_completed_orders_count * 100)
                                , 2)
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()
        return on_time_delivery_rate
    return None

def calculate_quality_rating_average(vendor):
    """
    calculate quality rating average of a specified vendor
    """

    completed_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code, 
        status="completed",
        quality_rating__isnull=False
    )
    
    if completed_orders_count.exists() :
        avg_quality_rating = round(completed_orders_count.aggregate(
            Avg('quality_rating'))['quality_rating__avg'], 2)
        vendor.quality_rating_avg = avg_quality_rating
        vendor.save()
        return avg_quality_rating
    return None

def calculate_average_response_time(vendor):
    """
    calculate average response time of a specified vendor.
    """

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

    # Calculating average response time
    if calc_average_response_time :
        vendor.average_response_time = avg_response_time_in_hours 
        vendor.save()
        return avg_response_time_in_hours
    return None

def calculate_fulfillment_rate(vendor):
    """
    calculate fulfillment rate of a specified vendor.
    """

    fulfilled_orders_count = PurchaseOrder.objects.filter(
        vendor=vendor.vendor_code,
        status='completed',
        quality_rating__isnull=False  # Assuming quality_rating being present indicates successful fulfillment
    ).count()

    total_orders_count = PurchaseOrder.objects.filter(
        vendor__vendor_code=vendor.vendor_code
    ).count()

    # Calculate the fulfillment rate
    if total_orders_count > 0:
        calc_fulfillment_rate = fulfilled_orders_count / total_orders_count * 100
        vendor.fulfillment_rate = calc_fulfillment_rate 
        vendor.save()   
        return calc_fulfillment_rate
    return None
