# django中ContentType笔记

## 在django中ContentType的使用场景

1. 在权限管理中使用到了contenttype，因为django内置的权限管理系统是针对模型级别的，在权限的model中添加了contenttype这个字段，这个字段可以使用`get_for_model()`
这个函数传入一个模型就可以获取contenttype，进而实现了model和权限的关联。

2. contenttype还可以使用在一个模型关联很多模型的外键的情况，比如当一张表跟 n 张表动态地创建 ForeignKey 关系时，而不是创建太多列，因为数据表中会有很多空值。
ContentType 通过仅两列字段就实现了 n 张表的 ForeignKey 关系。
也就是要关联到其他表中的具体行的数据可以采用contenttype来完成。
比如有三个表的model是这样的
```python 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


# Create your models here.
class DegreeCourse(models.Model):
    """
    学位课程表
    """
    name = models.CharField(max_length=32)
    price_list = GenericRelation("PricePolicy")


class Course(models.Model):
    """
    普通课程表
    """
    name = models.CharField(max_length=32)
    price_list = GenericRelation("PricePolicy")


class PricePolicy(models.Model):
    """
    价格策略的表 不同的时长不同的价格
    """
    price = models.FloatField() # 价格
    period = models.IntegerField() # 时长

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
```
要动态的保存每个课程的价格时长表，需要关联到每一个课程表里的每一个课程，一般情况下我们会增加课程id这个字段来表示课程，这样如果有多个课程类型的话就要增加多个课程的id，会增加很多空行，优化下，我们可以采用增加一个type表来确定是那类课程，通过外键关联，那么表的结构可以设计成下面这样
PricePolicy:
id | price | period | object_id | type_id
type:
id | name
这样设计以后，就可以使用object_id加上模型的id确定一个课程。
在django中内置了contenttype这张表 这张表可以实现和type表一样的功能

contenttype有id app_labal model 这三个字段，id代表主键，app_labal表示的是app的名字，model表示的是模型的名字，通过id就可以确定一个model，再添加一个id字段就可以确定课程表下面的哪个课程。

具体实现是通过`from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey`的`GenericRelation` 和 `GenericForeignKey` 来实现的，
`GenericRelation`是用来反向获取对象的集合，接收一个模型的名字作为反向查询的模型。
`GenericForeignKey`是用来关联contenttype和object_id的，关联以后就可以直接使用`content_object`来查询或者添加数据。
示例代码：
```python
class PricePolicy(models.Model):
    """
    价格策略的表 不同的时长不同的价格
    """
    price = models.FloatField() # 价格
    period = models.IntegerField() # 时长
    # 生成contenttype_id 确定哪个模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # 生成object_id 确定模型的哪条数据 
    object_id = models.IntegerField()
    # 用做关联模型和模型里面的数据的
    content_object = GenericForeignKey("content_type", "object_id")
```
那么在添加一条数据的时候，就可以使用下面的代码了：
```python 
    # 1.为学位课“Python全栈”添加一个价格策略：一个月9.9
    degreecourse = DegreeCourse.objects.filter(name="vue").first()
    PricePolicy.objects.create(price=9.9,period=30,content_object=degreecourse)
```
如果要获取学位课程的价格列表可以使用如下代码：
```python 
# 获取vue课程的价格列表
degreecourse = DegreeCourse.objects.filter(name="vue").first()
print(degreecourse.price_list.all())
```
删除和更新操作与常规模型操作是一样的
