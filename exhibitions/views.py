from django.shortcuts import render, get_object_or_404
from .models import Exhibition


def exhibition_list(request):
    exhibitions = Exhibition.objects.filter(do_not_show=False)
    return render(request, "exhibitions/exhibition_list.html", {"exhibitions": exhibitions})


def exhibition_detail(request, pk):
    exhibition = get_object_or_404(Exhibition, pk=pk)
    return render(request, "exhibitions/exhibition_detail.html", {"exhibition": exhibition})

