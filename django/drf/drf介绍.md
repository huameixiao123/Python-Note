# DRF介绍
## DRF介绍：
`DRF`是`Django Rest Framework`单词的简写，是在`Django`框架中实现`Restful API`的一个插件，使用他可以非常方便的实现接口数据的返回。`Django`中也可以使用`JsonResponse`直接返回`json`格式的数据，但是`DRF`相比直接使用`Django`返回`json`数据有以下几个好处：
1. 可以自动生成`API`文档，在前后端分离开发的时候进行沟通比较有用。
2. 授权验证策略比较完整，包含`OAuth1`和`OAuth2`验证。
3. 支持`ORM`模型和非`ORM`数据的序列化。
4. 高度封装了视图，使得返回`json`数据更加的高效。

## 安装：

`drf`目前最新的版本是`3.10`，需要以下依赖：
1. `Python (3.5, 3.6, 3.7)`
2. `Django (1.11, 2.0, 2.1, 2.2)`
准备好以上依赖后，可以通过`pip install djangorestframework`安装最新的版本。当然为了跟课程中的环境保持一致，可以安装`3.10`的版本。

## 基本使用：

### 一、注册`rest_framework`：
安装完后，使用他还需要进行在`settings.INSTALLED_APPS`中进行安装。
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```
### 二、创建app和模型：
创建一个名叫`meituan`的`app`，然后在`meituan.models`中创建以下模型：
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

创建完模型后，运行`makemigrations`和`migrate`后把模型映射到`mysql`数据库中。然后在`navicat`中，把`meituan_merchant.sql`文件运行后，添加测试数据。

### 四、编写Serializers：
在`meituan`这个`app`中新创建一个文件`serializers.py`，然后添加以下代码：
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
使用`drf`我们可以非常方便的创建包含`get/post`等`method`的视图。在`meituan.views`中添加以下代码：
```python
class MerchantViewSet(ModelViewSet):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
```
### 六、编写路由：
在`meituan.urls`中添加以下代码：
```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register('merchant',views.MerchantViewSet,basename='merchant')

urlpatterns = [
] + router.urls
```
然后再在项目的`urls.py`中把`meituan`的路由添加进去：
```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meituan/',include("meituan.urls"))
]
```
以后我们就可以使用不同的`method`向`/meituan/merchant`发送请求。比如用`get`，那么就会返回`merchant`的列表，比如用`post`，那么就会向`merchant`表添加数据。