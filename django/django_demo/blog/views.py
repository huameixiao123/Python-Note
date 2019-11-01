from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Category
from datetime import datetime


def index(request):
    return render(request, "index.html")


def add_article(request):
    category = Category.objects.create(name="Python")
    article = Article(title="sadas", content="dddd", author_id=1)
    article.category = category
    article.save()
    return HttpResponse("添加文章成功")


def update_article(request):
    article = Article.objects.first()
    article.title = "更新"
    article.save()
    return HttpResponse("文章更新成功")
