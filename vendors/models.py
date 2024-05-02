import uuid
from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    on_time_delivery_rate = models.FloatField(blank=True, default=0.0)
    quality_rating_avg = models.FloatField(blank=True, default=0.0)
    average_response_time = models.FloatField(blank=True, default=0.0)
    fulfillment_rate = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return self.name
