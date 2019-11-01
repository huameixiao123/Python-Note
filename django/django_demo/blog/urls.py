from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("add/", views.add_article, name="add_article"),
    path("update/", views.update_article, name="update_article"),
]
