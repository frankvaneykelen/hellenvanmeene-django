from xml.etree import ElementTree

import requests as http_requests
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


def home(request):
    from galleries.models import Gallery
    galleries = (
        Gallery.objects
        .filter(do_not_show=False)
        .select_related("place", "place__country")
    )
    return render(request, "home.html", {"galleries": galleries})


def search(request):
    q = request.GET.get("q", "").strip()
    results = {}

    if q:
        from exhibitions.models import Exhibition
        from events.models import Event
        from news.models import NewsArticle
        from publications.models import Publication
        from pages.models import Page

        results["exhibitions"] = Exhibition.objects.filter(
            do_not_show=False
        ).filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q)
        ).only("title", "subtitle", "foldername", "date_from_year")

        results["events"] = Event.objects.filter(
            do_not_show=False
        ).filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q)
        ).only("title", "subtitle", "foldername", "date_from_year")

        results["news"] = NewsArticle.objects.filter(
            do_not_show=False
        ).filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q) | Q(summary__icontains=q)
        ).only("title", "subtitle", "foldername", "publication_datetime")

        results["publications"] = Publication.objects.filter(
            do_not_show=False
        ).filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q)
            | Q(description__icontains=q) | Q(publisher__icontains=q)
        ).only("title", "subtitle", "foldername", "date_year")

        results["pages"] = Page.objects.filter(
            do_not_show=False
        ).filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q)
        ).only("title", "subtitle", "foldername")

        from links.models import Link
        results["links"] = Link.objects.filter(
            do_not_show=False
        ).filter(
            Q(label__icontains=q) | Q(description__icontains=q) | Q(url__icontains=q)
        ).only("label", "url", "description")

        section_keys = ("exhibitions", "events", "news", "publications", "pages", "links")
        results["total"] = sum(results[k].count() for k in section_keys)

    return render(request, "search_results.html", {"q": q, "results": results})


@staff_member_required
def blob_autocomplete(request):
    """
    Return up to 20 blob URLs whose filename contains the ``q`` query parameter.

    ``container_url`` must be passed as a query param — the full public URL of
    the blob container, e.g.
    ``https://hellenvanmeene.blob.core.windows.net/website-images``.

    Results are cached for 5 minutes.
    """
    q = request.GET.get("q", "").lower().strip()
    container_url = request.GET.get("container_url", "").rstrip("/")

    if not container_url:
        return JsonResponse(
            {"results": [], "error": "container_url parameter is required"}, status=400
        )

    cache_key = f"blob_list_{container_url}"
    all_names = cache.get(cache_key)

    if all_names is None:
        params = {"restype": "container", "comp": "list", "maxresults": 5000}
        try:
            resp = http_requests.get(container_url, params=params, timeout=10)
            resp.raise_for_status()
            root = ElementTree.fromstring(resp.text)
            all_names = [
                blob.find("Name").text
                for blob in root.iter("Blob")
                if blob.find("Name") is not None
            ]
            cache.set(cache_key, all_names, timeout=300)  # 5 min
        except Exception as exc:
            return JsonResponse({"results": [], "error": str(exc)}, status=502)

    if q:
        matched = [n for n in all_names if q in n.lower()]
    else:
        matched = all_names

    results = [f"{container_url}/{n}" for n in matched[:20]]
    return JsonResponse({"results": results})
