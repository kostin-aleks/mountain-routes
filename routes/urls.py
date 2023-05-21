"""routes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.urls import include, path
from routes.mountains.views import routes
from routes.user.views import user_profile
from .views import switch_language


urlpatterns = [
    path('', routes),
    path('login/', LoginView.as_view(
        template_name='registration/login.html'), name="login"),
    path('logout/', LogoutView.as_view(
        next_page='home'), name='log-out'),
    path('admin/', admin.site.urls),
    path('home/', routes, name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('mountains/', include('routes.mountains.urls')),
    path('user/', include('routes.user.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user_profile, name='account-profile'),
    path('switch/language/<language>/', switch_language, name='switch-language'),
    path('captcha', include("captcha.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
