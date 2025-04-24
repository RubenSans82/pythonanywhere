# mysite/mysite/urls.py

from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from daycare import views as daycare_views
from daycare.views import CustomLoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # La línea path('accounts/', include('django.contrib.auth.urls')), DEBE seguir eliminada.

    path('', daycare_views.landing_page, name='landing_page'),
    path('daycare/', include('daycare.urls')),

    # URLs de Autenticación de Django - Definidas manualmente
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('landing_page')), name='logout'),

    # --- URLs de Reseteo de Contraseña (Añadir estas líneas) ---
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # uidb64 y token son partes de la URL para confirmar el reseteo
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Nota: La última vista se llama PasswordCompleteView
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # --- Fin URLs de Reseteo de Contraseña ---
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)