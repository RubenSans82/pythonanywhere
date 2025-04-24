# mysite/mysite/urls.py

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from daycare import views as daycare_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', daycare_views.landing_page, name='landing_page'),
    path('daycare/', include('daycare.urls')), # <--- Asegúrate de incluir las URLs de daycare
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)