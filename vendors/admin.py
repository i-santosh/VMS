from django.contrib import admin
from .models import Vendor, HistoricalPerformance

"""
Registering Vendor Model
"""
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_details", "vendor_code"]

"""
Registering Historical Performance Model
"""                 
@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ["vendor", "date", "on_time_delivery_rate", 
                    "quality_rating_avg", "average_response_time", 
                    "fulfillment_rate"]