from django.shortcuts import render, get_object_or_404
from .models import Publication, PublicationType


def publication_list(request):
    pub_type = request.GET.get("type")
    year = request.GET.get("year")

    types = PublicationType.objects.all()
    years = (
        Publication.objects
        .filter(do_not_show=False, date_year__isnull=False)
        .values_list("date_year", flat=True)
        .distinct()
        .order_by("-date_year")
    )

    publications = (
        Publication.objects
        .filter(do_not_show=False)
        .select_related("publication_type", "publication_format", "place")
        .prefetch_related("publication_creators__creator")
    )
    if pub_type:
        publications = publications.filter(publication_type__label=pub_type)
    if year:
        publications = publications.filter(date_year=year)

    return render(request, "publications/publication_list.html", {
        "publications": publications,
        "types": types,
        "years": years,
        "active_type": pub_type,
        "active_year": year,
    })


def publication_detail(request, foldername):
    publication = get_object_or_404(
        Publication.objects.select_related("publication_type", "publication_format", "place")
        .prefetch_related("publication_creators__creator"),
        foldername=foldername,
    )
    return render(request, "publications/publication_detail.html", {"publication": publication})

