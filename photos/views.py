from django.shortcuts import render, get_object_or_404
from .models import Photo


def photo_list(request):
    photos = Photo.objects.filter(show=True, public=True)
    return render(request, "photos/photo_list.html", {"photos": photos})


def photo_detail(request, code):
    photo = get_object_or_404(Photo, code=code)
    return render(request, "photos/photo_detail.html", {"photo": photo})

