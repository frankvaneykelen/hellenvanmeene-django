from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("photos.urls")),
    path("exhibitions/", include("exhibitions.urls")),
    path("events/", include("events.urls")),
    path("news/", include("news.urls")),
    path("publications/", include("publications.urls")),
    path("shop/", include("shop.urls")),
    path("", include("pages.urls")),
]

# Serve media locally in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
