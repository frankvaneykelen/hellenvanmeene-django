from django.shortcuts import render, get_object_or_404
from .models import Exhibition


def exhibition_list(request):
    exhibitions = Exhibition.objects.filter(do_not_show=False).select_related(
        "location", "location__place", "exhibition_type", "language",
    )
    return render(request, "exhibitions/exhibition_list.html", {"exhibitions": exhibitions})


def exhibition_detail(request, foldername):
    exhibition = get_object_or_404(
        Exhibition.objects.select_related(
            "location", "location__place", "exhibition_type", "language", "editor",
        ).prefetch_related(
            "exhibition_creators__creator__role",
            "exhibition_media__photo",
            "exhibition_tags__tag",
            "exhibition_publications__publication",
        ),
        foldername=foldername,
    )
    return render(request, "exhibitions/exhibition_detail.html", {"exhibition": exhibition})

