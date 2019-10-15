## django中如何实现数据库的读写分离

### 读写分离
其基本原理就是让主数据库处理事务性增,改,删操作(INSERT,UPDATE,DELETE)操作,而从数据库处理SELECT查询操作,数据库复制被用来把事物性操作导致的变更同步到其他从数据库,以SQL为例,主数据库负责写数据,读数据,读库仅负责读数据,每次有写库操作,同步更新到读库,写库就一个,读库可以有多个,采用日志同步的方式实现主库和多个数据库的数据同步

### 使用

1. 在Django的配置文件settings.py中,DATABASES中添加代码如下:
```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 主服务器的运行ip
        'PORT': 3306,   # 主服务器的运行port
        'USER': 'django',  # 主服务器的用户名
        'PASSWORD': 'django',  # 主服务器的密码
        'NAME': 'djangobase'   #  数据表名
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql', 
        'HOST': '127.0.0.1',
        'PORT': 8306,
        'USER': 'django_slave',
        'PASSWORD': 'django_slave',
        'NAME': 'djangobase_slave'
    }
}　　
```
2. 创建数据库操作的路由分类
在项目的utils中创建db_router.py文件,并在该文件中定义一个db类,用来进行读写分离
```python 
class MasterSlaveDBRouter(object):
    """数据库主从读写分离路由"""
 
    def db_for_read(self, model, **hints):
        """读数据库"""
        return "slave"
 
    def db_for_write(self, model, **hints):
        """写数据库"""
        return "default"
 
    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True　　
```
3. 配置读写分离路由
`DATABASE_ROUTERS = ['项目名.utils.db_router."自定义的类名称"']`

### 也可以手动的进行数据的读写的分离

```python 
>>> # This will run on the 'default' database.
>>> Author.objects.all()

>>> # So will this.
>>> Author.objects.using('default').all()

>>> # This will run on the 'other' database.
>>> Author.objects.using('other').all()

>>> my_object.save(using='legacy_users')
```

### 在多个数据库中使用原始游标
```python 
from django.db import connections
with connections['my_db_alias'].cursor() as cursor:
    pass
````