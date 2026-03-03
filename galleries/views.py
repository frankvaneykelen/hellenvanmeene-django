from django.shortcuts import render
from .models import Gallery


def gallery_list(request):
    galleries = (
        Gallery.objects
        .filter(do_not_show=False)
        .select_related("place", "place__country")
    )
    return render(request, "galleries/gallery_list.html", {"galleries": galleries})
