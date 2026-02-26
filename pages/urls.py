from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("<str:foldername>/", views.page_detail, name="detail"),
]

