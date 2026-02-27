from django.shortcuts import render, get_object_or_404
from .models import Page


def page_detail(request, foldername):
    page = get_object_or_404(Page, foldername=foldername, do_not_show=False)
    return render(request, "pages/page_detail.html", {"page": page})

