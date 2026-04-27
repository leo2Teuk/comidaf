from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin désactivé — redirection vers le dashboard personnalisé
    path('admin/', RedirectView.as_view(url='/dashboard/', permanent=False)),
    # Auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='account_logout'),
    path('accounts/signup/', auth_views.LoginView.as_view(template_name='account/signup.html'), name='account_signup'),
    # App URLs
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

