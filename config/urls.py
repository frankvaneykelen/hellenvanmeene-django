from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import blob_autocomplete

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path("admin/blob-autocomplete/", blob_autocomplete, name="blob-autocomplete"),
    path("admin/", admin.site.urls),
    path("exhibitions/", include("exhibitions.urls")),
    path("events/", include("events.urls")),
    path("news/", include("news.urls")),
    path("publications/", include("publications.urls")),
    path("shop/", include("shop.urls")),
    path("photos/", include("photos.urls")),
    path("galleries/", include("galleries.urls")),
    path("links/", include("links.urls")),
    path("", include("core.urls")),
    path("", include("pages.urls")),
]

# Serve media locally in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
