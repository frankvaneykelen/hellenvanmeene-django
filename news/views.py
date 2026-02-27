from django.shortcuts import render, get_object_or_404
from .models import NewsArticle


def news_list(request):
    articles = NewsArticle.objects.filter(do_not_show=False)
    return render(request, "news/news_list.html", {"articles": articles})


def news_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, "news/news_detail.html", {"article": article})

