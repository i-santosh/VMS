from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', include("vendors.urls")),
    path('api/purchase_orders/', include("purchase_order.urls")),
]
