from django.urls import path
from . import views

app_name = "exhibitions"

urlpatterns = [
    path("", views.exhibition_list, name="list"),
    path("<slug:foldername>/", views.exhibition_detail, name="detail"),
]

