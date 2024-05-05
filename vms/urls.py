from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, 
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin
    path('api/vendors/', include("vendors.urls")),  # Vendor API
    path('api/purchase_orders/', include("purchase_order.urls")),  # Purchase Order API
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get JWT
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
]
