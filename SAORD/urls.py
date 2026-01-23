from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),

    # === api ===
    path('api/', include('core.api.urls_api')),
]
