from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('healthcare_dashboard.accounts.urls')),
    path('patients/', include('healthcare_dashboard.patients.urls')),
    path('doctors/', include('healthcare_dashboard.doctors.urls')),
    path('appointments/', include('healthcare_dashboard.appointments.urls')),
    path('pharmacy/', include('healthcare_dashboard.pharmacy.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)