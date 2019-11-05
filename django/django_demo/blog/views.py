from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def get_pagination_data(page, paginator, around_count=2):
    # 获取当前的页码
    current_page = page.number
    # 判断左边是否有更多
    left_has_more = False
    # 判断右边是否有更多
    right_has_more = False
    # 获取左边的页码区间
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)
    # 获取右边的页码区间
    if current_page >= paginator.num_pages - 3:
        right_pages = range(current_page + 1, paginator.num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + 3)
    return {
        "left_pages": left_pages,
        "right_pages": right_pages,
        "right_has_more": right_has_more,
        "left_has_more": left_has_more
    }


def index(request):
    # 获取分页的页码，默认是第一页
    number = request.GET.get("page", 1)
    # 将QuerySet对像封装成paginator对象
    paginator = Paginator(Article.objects.all(), per_page=10)
    # 获取当前页的Page对象
    page = paginator.get_page(number)
    # 获取分页参数
    pagination_data = get_pagination_data(page, paginator)
    context = {
        "paginator": paginator,
        "page": page
    }
    context.update(pagination_data)
    return render(request, "index.html", context=context)


def add_article(request):
    articles = []
    for i in range(102):
        article = Article(title="title%s" % i, content="content%s" % i)
        article.author = User.objects.first()
        article.category = Category.objects.first()
        articles.append(article)
    Article.objects.bulk_create(articles)
    return HttpResponse("添加文章成功")


def update_article(request):
    article = Article.objects.first()
    article.title = "更新"
    article.save()
    return HttpResponse("文章更新成功")
