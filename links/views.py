from django.shortcuts import render
from .models import Link


def links_list(request):
    links = Link.objects.filter(do_not_show=False)
    return render(request, "links/links_list.html", {"links": links})
