from django.shortcuts import render, get_object_or_404
from .models import Publication


def publication_list(request):
    publications = Publication.objects.filter(do_not_show=False)
    return render(request, "publications/publication_list.html", {"publications": publications})


def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, "publications/publication_detail.html", {"publication": publication})

