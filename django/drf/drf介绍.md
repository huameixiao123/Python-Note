# DRF介绍
## DRF介绍：
DRF是Django Rest Framework单词的简写，是在Django框架中实现Restful API的一个插件，使用他可以非常方便的实现接口数据的返回。Django中也可以使用JsonResponse直接返回json格式的数据，但是DRF相比直接使用Django返回json数据有以下几个好处：
1. 可以自动生成API文档，在前后端分离开发的时候进行沟通比较有用。
2. 授权验证策略比较完整，包含OAuth1和OAuth2验证。
3. 支持ORM模型和非ORM数据的序列化。
4. 高度封装了视图，使得返回json数据更加的高效。

## 安装：

drf目前最新的版本是3.10，需要以下依赖：
1. Python (3.5, 3.6, 3.7)
2. Django (1.11, 2.0, 2.1, 2.2)
准备好以上依赖后，可以通过pip install djangorestframework安装最新的版本。当然为了跟课程中的环境保持一致，可以安装3.10的版本。

## 基本使用：

### 一、注册rest_framework：
安装完后，使用他还需要进行在settings.INSTALLED_APPS中进行安装。
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```
### 二、创建app和模型：
创建一个名叫meituan的app，然后在meituan.models中创建以下模型：
```python
from django.db import models
from django.contrib.auth.models import User

class Merchant(models.Model):
    """
    商家
    """
    name = models.CharField(max_length=200,verbose_name='商家名称',null=False)
    address = models.CharField(max_length=200,verbose_name='商家',null=False)
    logo = models.CharField(max_length=200,verbose_name='商家logo',null=False)
    notice = models.CharField(max_length=200, verbose_name='商家的公告',null=True,blank=True)
    up_send = models.DecimalField(verbose_name='起送价',default=0,max_digits=6,decimal_places=2)
    lon = models.FloatField(verbose_name='经度')
    lat = models.FloatField(verbose_name='纬度')

    created = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)


class GoodsCategory(models.Model):
    """
    商家商品分类
    """
    name = models.CharField(max_length=20,verbose_name='分类名称')
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,verbose_name='所属商家',related_name='categories')

class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=200,verbose_name='商品名称')
    picture = models.CharField(max_length=200,verbose_name='商品图片')
    intro = models.CharField(max_length=200)
    price = models.DecimalField(verbose_name='商品价格',max_digits=6,decimal_places=2) # 最多6位数，2位小数。9999.99
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,related_name='goods_list')
```
### 三、添加测试数据：

创建完模型后，运行makemigrations和migrate后把模型映射到mysql数据库中。然后在navicat中，把meituan_merchant.sql文件运行后，添加测试数据。

### 四、编写Serializers：
在meituan这个app中新创建一个文件serializers.py，然后添加以下代码：
```python
from rest_framework import serializers
from .models import Merchant,GoodsCategory,Goods

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"
```
### 五、编写视图：
使用drf我们可以非常方便的创建包含get/post等method的视图。在meituan.views中添加以下代码：
```python
class MerchantViewSet(ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
```
### 六、编写路由：
在meituan.urls中添加以下代码：
```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register('merchant',views.MerchantViewSet,basename='merchant')

urlpatterns = [
] + router.urls
然后再在项目的urls.py中把meituan的路由添加进去：

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meituan/',include("meituan.urls"))
]
```
以后我们就可以使用不同的method向/meituan/merchant发送请求。比如用get，那么就会返回merchant的列表，比如用post，那么就会向merchant表添加数据。