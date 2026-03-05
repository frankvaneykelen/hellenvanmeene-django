from django.shortcuts import render
from django.db.models import ExpressionWrapper, F, IntegerField
from .models import Link


def links_list(request):
    links = (
        Link.objects
        .filter(do_not_show=False)
        .annotate(
            effective_order=ExpressionWrapper(
                F("id") + F("boost"), output_field=IntegerField()
            )
        )
        .order_by("-effective_order")
    )
    return render(request, "links/links_list.html", {"links": links})
