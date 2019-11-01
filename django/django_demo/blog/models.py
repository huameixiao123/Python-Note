from django.db import models
from Mixins.model import BaseModel
from django.contrib.auth.models import User


class Article(BaseModel):
    """
    文章表
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, default="", related_name="articles")


class Category(BaseModel):
    """
    分类表
    """
    name = models.CharField(max_length=30)
