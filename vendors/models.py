from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, primary_key=True)
    on_time_delivery_rate = models.FloatField(blank=True, default=0.0)
    quality_rating_avg = models.FloatField(blank=True, default=0.0)
    average_response_time = models.FloatField(blank=True, default=0.0)
    fulfillment_rate = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return self.name

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.vendor.name
    
    @classmethod
    def add_performance_record(cls, 
                               vendor, 
                               on_time_delivery_rate=None, 
                               quality_rating_avg=None, 
                               average_response_time=None, 
                               fulfillment_rate=None):
        cls.objects.create(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )
