"""URL Configuration"""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico')),

    path('', include(('app_django.cars.urls', 'cars'), namespace='cars')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
