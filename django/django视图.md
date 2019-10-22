# Django限制请求method

## 常用的请求method

1. GET请求：GET请求一般用来向服务器索取数据，但不会向服务器提交数据，不会对服务器的状态进行更改。比如向服务器获取某篇文章的详情。
2. POST请求：POST请求一般是用来向服务器提交数据，会对服务器的状态进行更改。比如提交一篇文章给服务器。

## 限制请求装饰器

1. `Django `内置的视图装饰器可以给视图提供一些限制。比如这个视图只能通过 `GET `的 `method `访问等。以下将介绍一些常用的内置视图装饰器。
```python
    from django.views.decorators.http import require_http_methods
    
    @require_http_methods(["GET"])
    def my_view(request):
        pass
```
2. `django.views.decorators.http.require_GET` ：这个装饰器相当于是 `require_http_methods(['GET'])` 的简写形式，只允许使用 `GET `的 `method `来访问视图。示例代码如下：
```python
    from django.views.decorators.http import require_GET
    
    @require_GET
    def my_view(request):
        pass
```
3. `django.views.decorators.http.require_POST` ：这个装饰器相当于是 `require_http_methods(['POST'])` 的简写形式，只允许使用 `POST `的 `method `来访问视图。示例代码如下：
```python
    from django.views.decorators.http import require_POST
    
    @require_POST
    def my_view(request):
        pass
```
4. `django.views.decorators.http.require_safe` ：这个装饰器相当于是 `require_http_methods(['GET','HEAD'])` 的简写形式，只允许使用相对安全的方式来访问视图。因为 `GET `和 `HEAD `不会对服务器产生增删改的行为。因此是一种相对安全的请求方式。示例代码如下：
```python
    from django.views.decorators.http import require_safe
    
    @require_safe
    def my_view(request):
        pass
```

# 重定向

重定向分为永久性重定向和暂时性重定向，在页面上体现的操作就是浏览器会从一个页面自动跳转到另外一个页面。比如用户访问了一个需要权限的页面，但是该用户当前并没有登录，因此我们应该给他重定向到登录页面。
+ 永久性重定向：http的状态码是301，多用于旧网址被废弃了要转到一个新的网址确保用户的访问，最经典的就是京东网站，你输入www.jingdong.com的时候，会被重定向到www.jd.com，因为jingdong.com这个网址已经被废弃了，被改成jd.com，所以这种情况下应该用永久重定向。
- 暂时性重定向：http的状态码是302，表示页面的暂时性跳转。比如访问一个需要权限的网址，如果当前用户没有登录，应该重定向到登录页面，这种情况下，应该用暂时性重定向。
在 `Django `中，重定向是使用 `redirect(to, *args, permanent=False, **kwargs)` 来实现的。 `to `是一个 `url `， `permanent `代表的是这个重定向是否是一个永久的重定向，默认是 `False `。关于重定向的使用。请看以下例子：
```python
    from django.shortcuts import reverse,redirect
    from django.http import HttpResponse
    
    def profile(request):
        if request.GET.get("username"):
            return HttpResponse("%s，欢迎来到个人中心页面！")
        else:
            return redirect(reverse("user:login"))
```

# WSGIRequest对象

`Django`在接收到`http`请求之后，会根据`http`请求携带的参数以及报文信息创建一个 `WSGIRequest`对象，并且作为视图函数第一个参数传给视图函数。也就是我们经常看到的 `request `参数。在这个对象上我们可以找到客户端上传上来的所有信息。这个对象的完整路径是 `django.core.handlers.wsgi.WSGIRequest` 。

## WSGIRequest对象常用属性和方法

### WSGIRequest对象常用属性

WSGIRequest 对象上大部分的属性都是只读的。因为这些属性是从客户端上传上来的，没必要做任何的修改。以下将对一些常用的属性进行讲解：
1. `path`：请求服务器的完整“路径”，但不包含域名和参数。比如 `http://www.baidu.com/xxx/yyy/` ，那么 `path `就是 `/xxx/yyy/` 。
2. `method`：代表当前请求的 `http `方法。比如是 `GET `还是 `POST `。
3. `GET`：一个 `django.http.request.QueryDict` 对象。操作起来类似于字典。这个属性中包含了所有以 `?xxx=xxx` 的方式上传上来的参数。
4. `POST`：也是一个 `django.http.request.QueryDict` 对象。这个属性中包含了所有以 POST 方式上传上来的参数。
5. `FILES`：也是一个 `django.http.request.QueryDict` 对象。这个属性中包含了所有上传的文件。
6. `COOKIES` ：一个标准的Python字典，包含所有的 `cookie`，键值对都是字符串类型。
7. `session`：一个类似于字典的对象。用来操作服务器的 `session`。
8. `META`：存储的客户端发送上来的所有 header 信息。
    +  `CONTENT_LENGTH`：请求的正文的长度（是一个字符串）。
    +  `CONTENT_TYPE` ：请求的正文的MIME类型。
    + `HTTP_ACCEPT`：响应可接收的Content-Type。
    + `HTTP_ACCEPT_ENCODING`：响应可接收的编码。
    + `HTTP_ACCEPT_LANGUAGE`： 响应可接收的语言。
    + `HTTP_HOST`：客户端发送的HOST值。
    + `HTTP_REFERER`：在访问这个页面上一个页面的url。
    + `QUERY_STRING`：单个字符串形式的查询字符串（未解析过的形式）。
    + `REMOTE_HOST`：客户端的主机名。
    + `REQUEST_METHOD`：请求方法。一个字符串类似于 `GET`或者 `POST`。
    + `SRVER_NAME `：服务器域名。
    + `SERVER_PORT`：服务器端口号，是一个字符串类型。
    + `REMOTE_ADDR`：客户端的IP地址。如果服务器使用了 nginx 做反向代理或者负载均衡，那么这个值返回的是 127.0.0.1 ，这时候可以使用 `HTTP_X_FORWARDED_FOR`来获取，所以获取 `ip`地址的代码片段如下:

```python
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
```


### WSGIRequest对象常用方法

1. `is_secure()` ：是否是采用 `https `协议。
2. `is_ajax()` ：是否采用 `ajax `发送的请求。原理就是判断请求头中是否存在 `X-Requested-With:XMLHttpRequest` 。
3. `get_host()` ：服务器的域名。如果在访问的时候还有端口号，那么会加上端口号。比如 `www.baidu.com:9000` 。
4. `get_full_path()` ：返回完整的path。如果有查询字符串，还会加上查询字符串。比如 `/music/bands/?print=True` 。
5. `get_raw_uri()` ：获取请求的完整 `url `。

### QueryDict对象

我们平时用的 `request.GET` 和 `request.POST` 都是 `QueryDict`对象，这个对象继承自 `dict`，因此用法跟 `dict`相差无几。其中用得比较多的是 `get`方法和 `getlist`方法。
1. `get`方法：用来获取指定 `key`的值，如果没有这个 `key`，那么会返回 `None`。
2. `getlist`方法：如果浏览器上传上来的 `key`对应的值有多个，那么就需要通过这个方法获取。

在`HttpRequest`对象中，`GET`和`POST`属性都是一个`django.http.QueryDict`的实例。`request.POST`或`request.GET`的`QueryDict`都是不可变的，只读的。如果要修改它，需要使用`QueryDict.copy()`方法，获取一个拷贝，然后在这个拷贝上进行修改操作。

**方法**
`QueryDict`实现了Python字典数据业的所有标准方法，因为它是字典的子类。不同之处有：

1. QueryDict.init(query_string=None,mutable=False,encoding=None)
```python
>>> QueryDict('a=1&a=2&c=3)
<QueryDict: {'a':['1','2'],'c':['3']}>
```
如果需要实例化可以修改的对象，添加参数`mutable=True`。

2. classmethod QueryDict.fromkeys(itrable,value='',mutable=False,encoding=None)
Django1.11中的新功能。循环可迭代对象中每个元素作为键值，并赋予同样的值（来自`value`参数）
```python
>>> QueryDict.fromkeys(['a', 'a', 'b'], value='val')
<QueryDict: {'a': ['val', 'val'], 'b': ['val']}>
```

3. QueryDict.update(other_dict)
用新的QueryDict或字典更新当前QueryDict。类似dict.update()，但是追加内容，而不是更新并替换它们。 像这样：
```python
>>> q = QueryDict('a=1', mutable=True)
>>> q.update({'a': '2'})
>>> q.getlist('a')
['1', '2']
>>> q['a'] # returns the last
'2'
```

4. QueryDict.items()
类似`dict.items()`，如果有重复项目，返回最近的一个，而不是都返回：
```python
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.items()
[('a', '3')]
```

5. QueryDict.values()
类似dict.values()，但是只返回最近的值。 像这样：
```python
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.values()
['3']
```

6. QueryDict.copy()
使用`copy.deepcopy()`返回`QueryDict`对象的副本。 此副本是可变的！

7. QueryDict.getlist(key, default=None)
返回键对应的值列表。 如果该键不存在并且未提供默认值，则返回一个空列表。

8. QueryDict.setlist(key, list_)
为`list`设置给定的键。

9. QueryDict.appendlist(key, item)
将键追加到内部与键相关联的列表中。

10. QueryDict.setdefault(key, default=None)
类似`dict.setdefault()`，为某个键设置默认值。

11. QueryDict.setlistdefault(key, default_list=None)
类似setdefault()，除了它需要的是一个值的列表而不是单个值。

12. QueryDict.lists()
类似`items()`，只是它将其中的每个键的值作为列表放在一起。 像这样：
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.lists()
[('a', ['1', '2', '3'])]

13. QueryDict.pop(key)
返回给定键的值的列表，并从QueryDict中移除该键。 如果键不存在，将引发KeyError。 像这样：
```python
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.pop('a')
['1', '2', '3']
```

14. QueryDict.popitem()
删除`QueryDict`任意一个键，并返回二值元组，包含键和键的所有值的列表。在一个空的字典上调用时将引发`KeyError`。 像这样：
```python
>>> q = QueryDict('a=1&a=2&a=3', mutable=True)
>>> q.popitem()
('a', ['1', '2', '3'])
```

15. QueryDict.dict()
将`QueryDict`转换为Python的字典数据类型，并返回该字典。如果出现重复的键，则将所有的值打包成一个列表，最为新字典中键的值。
```python
>>> q = QueryDict('a=1&a=3&a=5')
>>> q.dict()
{'a': '5'}
```

16. QueryDict.urlencode(safe=None)
已url的编码格式返回数据字符串。 像这样：
```python
>>> q = QueryDict('a=2&b=3&b=5')
>>> q.urlencode()
'a=2&b=3&b=5'
```
使用safe参数传递不需要编码的字符。 像这样：
```python
>>> q = QueryDict(mutable=True)
>>> q['next'] = '/a&b/'
>>> q.urlencode(safe='/')
'next=/a%26b/'
```
# HttpResponse对象

`Django`服务器接收到客户端发送过来的请求后，会将提交上来的这些数据封装成一个 `HttpRequest`对象传给视图函数。那么视图函数在处理完相关的逻辑后，也需要返回一个响应
给浏览器。而这个响应，我们必须返回 `HttpResponseBase`或者他的子类的对象。而 `HttpResponse`则是 `HttpResponseBase`用得最多的子类。那么接下来就来介绍一下 `HttpResponse`及其子类。

## 常用属性

1. `content`：返回的内容。
2. `status_code`：返回的HTTP响应状态码。
3. `content_type`：返回的数据的MIME类型，默认为 `text/html` 。浏览器会根据这个属性，来显示数据。如果是 `text/html` ，那么就会解析这个字符串，如果`text/plain` ，那么就会显示一个纯文本。常用的 `Content-Type` 如下：
    + text/html（默认的，html文件）
    + text/plain（纯文本）
    + text/css（css文件）
    + text/javascript（js文件）
    + multipart/form-data（文件提交）
    + application/json（json传输）
    + application/xml（xml文件）
4. 设置请求头： `response['X-Access-Token'] = 'xxxx'` 。

## 常用方法

1. `set_cookie`：用来设置 `cookie`信息。后面讲到授权的时候会着重讲到。
2. `delete_cookie`：用来删除 `cookie`信息。
3. `write`： `HttpResponse`是一个类似于文件的对象，可以用来写入数据到数据体（**content**）中。


# JsonResponse类

用来对象 `dump`成 `json`字符串，然后返回将 `json` 字符串封装成 `Response`对象返回给浏览器。并且他的 `Content-Type` 是 `application/json` 。示例代码如下：
```python
    from django.http import JsonResponse
    
    def index(request):
        return JsonResponse({"username":"zhiliao","age":18})
```
默认情况下 `JsonResponse`只能对字典进行 `dump`，如果想要对非字典的数据进行 `dump`，那么需要给 `JsonResponse`传递一个 `safe=False` 参数。示例代码如下：
```python
    from django.http import JsonResponse
    
    def index(request):
        persons = ['张三','李四','王五']
        return HttpResponse(persons,safe=False)
```

## 文件上传

Django在处理文件上传时，文件数据被打包封装在request.FILES中。

### 一、简单上传

首先，写一个form模型，它必须包含一个FileField：
```python
# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
```
处理这个表单的视图将在`request.FILES`中收到文件数据，可以用`request.FILES['file']`来获取上传文件的具体数据，其中的键值‘`file`’是根据`file = forms.FileField()`的变量名来的。

注意：`request.FILES`只有在请求方法为POST,并且提交请求的`<form>`具有`enctype="multipart/form-data"`属性时才有效。 否则，`request.FILES`将为空。

下面是一个接收上传文件的视图范例：
```python
# views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# 另外写一个处理上传过来的文件的方法，并在这里导入
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 注意获取数据的方式
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
```
请注意，必须将request.FILES传递到form的构造函数中。
```python
form = UploadFileForm(request.POST, request.FILES)
```
下面是一个处理上传文件的方法的参考例子：
```python
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```
遍历`UploadedFile.chunks()`，而不是直接使用`read()`方法，能确保大文件不会占用系统过多的内存

---

### 二、使用模型处理上传的文件

如果是通过模型层的model来指定上传文件的保存方式的话，使用ModelForm更方便。 调用form.save()的时候，文件对象会保存在相应的`FileField`的``upload_to``参数指定的地方。
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ModelFormWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # 这么做就可以了，文件会被保存到Model中upload_to参数指定的位置
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})
```
如果手动构造一个对象，还可以简单地把文件对象直接从request.FILES赋值给模型：
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ModelWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
```

---

###  同时上传多个文件

如果要使用一个表单字段同时上传多个文件，需要设置字段HTML标签的`multiple`属性为True，如下所示：
```python
# forms.py

from django import forms

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
```
然后，自己编写一个FormView的子类，并覆盖它的post方法，来处理多个文件上传：
```python
# views.py
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # 用你的模版名替换.
    success_url = '...'  # 用你的URL或者reverse()替换.

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
```

---

### 上传文件处理器

当用户上传一个文件的时候，Django会把文件数据传递给上传文件处理器–一个类。上传处理器的配置定义在`FILE_UPLOAD_HANDLERS`中，默认为：
```python
["django.core.files.uploadhandler.MemoryFileUploadHandler", "django.core.files.uploadhandler.TemporaryFileUploadHandler"]
```
`MemoryFileUploadHandler`和`TemporaryFileUploadHandler`定义了Django的默认文件上传行为：将小文件读取到内存中，大文件放置在磁盘中。
在你保存上传文件之前，数据需要储存在某个地方。通常，如果上传文件小于2.5MB，Django会把整个内容存到内存。 这意味着，文件的保存仅仅涉及到内存中的读取和磁盘的写入，所以非常快。但是，如果上传的文件很大，Django会把它写入一个临时文件，储存在你的系统临时目录中。在类Unix的平台下，Django会生成一个文件，名称类似于`/tmp/tmpzfp6I6.upload`。

我们可以编写自定义的处理器，来定制Django如何处理文件。例如，根据级别不同限制用户的磁盘配额，在运行中压缩数据，渲染进度条，甚至是转存到另一个储存位置，而不把它存到本地。

# 生成CSV文件

有时候我们做的网站，需要将一些数据，生成有一个 `CSV`文件给浏览器，并且是作为附件的形式下载下来。以下将讲解如何生成 `CSV`文件。

## 生成小的CSV文件

这里将用一个生成小的 `CSV`文件为例，来把生成 `CSV`文件的技术要点讲到位。我们用 `Python`内置的 `csv`模块来处理 `csv`文件，并且使用 HttpResponse 来将 `csv`文件返回回去。示例代码如下：
```python
    import csv
    from django.http import HttpResponse
    
    def csv_view(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        writer.writerow(['username', 'age', 'height', 'weight'])
        writer.writerow(['zhiliao', '18', '180', '110'])
        
        return response
```
这里再来对每个部分的代码进行解释：
1. 我们在初始化 `HttpResponse`的时候，指定了 `Content-Type` 为 `text/csv` ，这将告诉浏览器，这是一个 `csv`格式的文件而不是一个 `HTML`格式的文件，如果用默认值，默认值就是 html ，那么浏览器将把 `csv`格式的文件按照 `html`格式输出，这肯定不是我们想要的。
2. 第二个我们还在 `response`中添加一个 `Content-Disposition` 头，这个东西是用来告诉浏览器该如何处理这个文件，我们给这个头的值设置为 `attachment;` ，那么浏览器将不会对这个文件进行显示，而是作为附件的形式下载，第二个 `filename="somefilename.csv"` 是用来指定这个 `csv`文件的名字。
3. 我们使用 `csv`模块的 `writer`方法，将相应的数据写入到 `response`中。
4. 写入中文乱码的时候，需要先导入`codecs`模块，`import codecs`,然后在`csv`写入数据之前增加语句`response.write(codecs.BOM_UTF8)`。

## 将`csv`文件定义成模板

我们还可以将 `csv`格式的文件定义成模板，然后使用 `Django`内置的模板系统，并给这个模板传入一个 `Context`对象，这样模板系统就会根据传入的 `Context`对象，生成具体的 `csv`文件。示例代码如下：
```python
    # 模板文件
    {% for row in rows %}
        "{{ row.0|addslashes }}", 
        "{{ row.1|addslashes }}", 
        "{{ row.2|addslashes }}", 
        "{{ row.3|addslashes }}", 
        "{{ row.4|addslashes }}"
    {% endfor %}
    
    # 视图函数
    from django.http import HttpResponse
    from django.template import loader
    
    def some_view(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        context = {
            'rows':(
                ('First row', 'Foo', 'Bar', 'Baz'),
                ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
            )
        }
        t = loader.get_template('my_template_name.txt')
        response.write(t.render(context))
        return response
```
注意：`context`中的关键字`rows`必须与模板中的`for`标签中的`rows`保持一致。

## 生成大的CSV文件

以上的例子是生成的一个小的 `csv`文件，如果想要生成大型的 `csv`文件，那么以上方式将有可能会发生超时的情况（服务器要生成一个大型csv文件，需要的时间可能会超过浏览器默认的超时时间）。这时候我们可以借助另外一个类，叫做 `StreamingHttpResponse`对象，这个对象是将响应的数据作为一个流返回给客户端，而不是作为一个整体返回。示例代码如下：
```python
    class Echo:
        """
        定义一个可以执行写操作的类，以后调用csv.writer的时候，就会执行这个方法
        """
        def write(self, value):
            return value
    def large_csv(request):
        rows = (["Row {}".format(idx), str(idx)] for idx in range(655360))    
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows),content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response
```
这里我们构建了一个非常大的数据集 `rows`，并且将其变成一个迭代器。然后因为 `StreamingHttpResponse`的第一个参数只能是一个生成器，因此我们使用圆括号 `(writer.writerow(row) for row in rows)` ，并且因为我们要写的文件是 csv 格式的文件，因此需要调用 `writer.writerow` 将 `row`变成一个 csv 格式的字符串。而调用 `writer.writerow` 又需要一个中间的容器，因此这里我们定义了一个非常简单的类 `Echo`，这个类只实现一个 `write`方法，以后在执行 `csv.writer(pseudo_buffer)` 的时候，就会调用 `Echo.writer` 方法。

### 关于StreamingHttpResponse

这个类是专门用来处理流数据的。使得在处理一些大型文件的时候，不会因为服务器处理时间过长而到时连接超时。这个类不是继承自 `HttpResponse`，而是继承自`HttpResponseBase`类，并且跟 `HttpResponse`对比有以下几点区别：
1. 这个类没有属性 `content`，相反是 `streaming_content`。
2. 这个类的 `streaming_content`必须是一个可以迭代的对象。
3. 这个类没有 `write`方法，如果给这个类的对象写入数据将会报错。
注意： `StreamingHttpResponse`会启动一个进程来和客户端保持长连接，所以会很消耗资源。所以如果不是特殊要求，尽量少用这种方法。

## 动态生成PDF文件

---

可以通过开源的Python PDF库`ReportLab`来实现PDF文件的动态生成。

---

### 一、安装ReportLab

ReportLab库在PyPI上提供，可以使用pip来安装：
```bash
$ pip install reportlab
```
在Python交互解释器中导入它来测试安装：
```python
>>> import reportlab
```
如果没有抛出任何错误，证明已安装成功。

---

### 二、编写视图

ReportLab的API可以处理于类似于文件（file-like）的对象。下面是一个 “Hello World”的例子：
```python
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # 创建带有PDF头部定义的HttpResponse对象
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # 创建一个PDF对象，并使用响应对象作为它要处理的‘文件’
    p = canvas.Canvas(response)

    # 通过PDF对象的drawString方法，写入一条信息。具体参考模块的官方文档说明。
    p.drawString(100, 100, "Hello world.")

    # 关闭PDF对象
    p.showPage()
    p.save()
    return response
```
相关说明：
+ 响应对象的MIME类型为`application/pdf`。 这会告诉浏览器，文档是个PDF文件而不是HTML文件。
+ 响应对象设置了附加的`Content-Disposition`协议头，含有PDF文件的名称。
+ 文件名可以是任意的，浏览器会在“另存为...”对话框等中使用。
+ `Content-Disposition`以'attachment'开头，强制让浏览器弹出对话框来提示或者确认。
+ Canvas函数接受一个类似于文件的对象，而HttpResponse对象正好合适。
+ 最后，在PDF文件上调用showPage()和save()方法非常重要。
+ 注意：ReportLab并不是线程安全的。

---


### 三、复杂的PDF

使用ReportLab创建复杂的PDF文档时，可以考虑使用io库作为PDF文件的临时保存地点。这个库提供了一个类似于文件的对象接口，非常实用。 下面的例子是上面的“Hello World”示例采用io重写后的样子：
```python
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
```

# 类视图

在写视图的时候， `Django`除了使用函数作为视图，也可以使用类作为视图。使用类视图可以使用类的一些特性，比如继承等。

## View

`django.views.generic.base.View`是主要的类视图，所有的类视图都是继承自它。如果我们写自己的类视图，也可以继承自它。然后再根据当前请求的 `method`，来实现不同的方法。比如这个视图只能使用 `get`的方式来请求，那么就可以在这个类中定义 `get(self,request,*args,**kwargs)` 方法。以此类推，如果只需要实现 `post`方法，那么就只需
要在类中实现 `post(self,request,*args,**kwargs)` 。示例代码如下：
```python
    from django.views import View
    
    class BookDetailView(View):
        def get(self,request,*args,**kwargs):
            return render(request,'detail.html')
```
类视图写完后，还应该在 `urls.py` 中进行映射，映射的时候就需要调用 `View`的类方法 `as_view()` 来进行转换。示例代码如下：
```python
    urlpatterns = [
        path("detail/<book_id>/",views.BookDetailView.as_view(),name='detail'),
    ]
```
除了 `get`方法， `View`还支持以下方法 `['get','post','put','patch','delete','head','options','trace']` 。
如果用户访问了 `View`中没有定义的方法。比如你的类视图只支持 get 方法，而出现了 `post`方法，那么就会把这个请求转发给`http_method_not_allowed(request,*args,**kwargs)` 。示例代码如下：
```python
    class AddBookView(View):
    def post(self,request,*args,**kwargs):
        return HttpResponse("书籍添加成功！")
        
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("您当前采用的method是：%s，本视图只支持使用post请求！" % request.method)
```
`urls.py` 中的映射如下:
```python
    path("addbook/",views.AddBookView.as_view(),name='add_book'),
```
如果你在浏览器中访问 `addbook/` ，因为浏览器访问采用的是 `get`方法，而 `addbook`只支持 `post`方法，因此以上视图会返回您当前采用的 `method`是： GET ，本视图只支持使用 `post`请求！。
其实不管是 `get`请求还是 `post`请求，都会走 `dispatch(request,*args,**kwargs)` 方法，所以如果实现这个方法，将能够对所有请求都处理到。

## TemplateView

`django.views.generic.base.TemplateView`，这个类视图是专门用来返回模版的。在这个类中，有两个属性是经常需要用到的，一个是 `template_name`，这个属性是用来存储模版的路径， `TemplateView`会自动的渲染这个变量指向的模版。另外一个是 `get_context_data`，这个方法是用来返回上下文数据的，也就是在给模版传的参数的。示例代码如下：
```python
    from django.views.generic.base import TemplateView
    
    class HomePageView(TemplateView):
        template_name = "home.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['username'] = "黄老师"
            return context
```
在 `urls.py` 中的映射代码如下：
```python
    from django.urls import path
    from myapp.views import HomePageView
    
    urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
    ]
```
如果在模版中不需要传递任何参数，那么可以直接只在 `urls.py` 中使用 `TemplateView`来渲染模版。示例代码如下：
```python
    from django.urls import path
    from django.views.generic import TemplateView
    
    urlpatterns = [
        path('about/', TemplateView.as_view(template_name="about.html")),
    ]
```

## ListView

在网站开发中，经常会出现需要列出某个表中的一些数据作为列表展示出来。比如文章列表，图书列表等等。在 `Django`中可以使用 `ListView`来帮我们快速实现这种需求。示例代码如下：
```python
    class ArticleListView(ListView):
        model = Article
        template_name = 'article_list.html'
        paginate_by = 10
        context_object_name = 'articles'
        ordering = 'create_time'
        page_kwarg = 'page'
        
        def get_context_data(self, **kwargs):
            context = super(ArticleListView, self).get_context_data(**kwargs)
            print(context)
            return context
        
        def get_queryset(self):
            return Article.objects.filter(id__lte=89)
```
对以上代码进行解释：
1. 首先 `ArticleListView`是继承自 `ListView`。
2. `model`：重写 `model`类属性，指定这个列表是给哪个模型的。
3. `template_name`：指定这个列表的模板。
4. `paginate_by`：指定这个列表一页中展示多少条数据。
5. `context_object_name`：指定这个列表模型在模板中的参数名称。
6. `ordering`：指定这个列表的排序方式。
7. `page_kwarg`：获取第几页的数据的参数名称。默认是 page 。
8. `get_context_data`：获取上下文的数据。
9. `get_queryset`：如果你提取数据的时候，并不是要把所有数据都返回，那么你可以重写这个方法。将一些不需要展示的数据给过滤掉。

## Paginator和Page类

`Paginator`和 `Page`类都是用来做分页的。他们在 `Django`中的路径为 `django.core.paginator.Paginator` 和 django.core.paginator.Page 。以下对这两个类的常用属性和方法做解释：

### Paginator常用属性和方法

1. `count`：总共有多少条数据。
2. `num_pages`：总共有多少页。
3. `page_range`：页面的区间。比如有三页，那么就 range(1,4) 。

### Page常用属性和方法

1. `has_next`：是否还有下一页。
2. `has_previous`：是否还有上一页。
3. `next_page_number`：下一页的页码。
4. `previous_page_number`：上一页的页码。
5. `number`：当前页。
6. `start_index`：当前这一页的第一条数据的索引值。
7. `end_index`：当前这一页的最后一条数据的索引值。

# 给类视图添加装饰器

在开发中，有时候需要给一些视图添加装饰器。如果用函数视图那么非常简单，只要在函数的上面写上装饰器就可以了。但是如果想要给类添加装饰器，那么可以通过以下两种方式来实现：

## 装饰dispatch方法

```python
    from django.utils.decorators import method_decorator
    
    def login_required(func):
        def wrapper(request,*args,**kwargs):
            if request.GET.get("username"):
                return func(request,*args,**kwargs)
            else:
                return redirect(reverse('index'))
        return wrapper
        
    class IndexView(View):
        def get(self,request,*args,**kwargs):
            return HttpResponse("index")
            
        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            super(IndexView, self).dispatch(request,*args,**kwargs)
```

## 直接装饰在整个类上

```python
    from django.utils.decorators import method_decorator
    
    def login_required(func):
        def wrapper(request,*args,**kwargs):
            if request.GET.get("username"):
                return func(request,*args,**kwargs)
            else:
                return redirect(reverse('login'))
        return wrapper
        
    @method_decorator(login_required,name='dispatch')
    class IndexView(View):
        def get(self,request,*args,**kwargs):
            return HttpResponse("index")
            
        def dispatch(self, request, *args, **kwargs):
            super(IndexView, self).dispatch(request,*args,**kwargs)
```

# 错误处理

在一些网站开发中。经常会需要捕获一些错误，然后将这些错误返回比较优美的界面，或者是将这个错误的请求做一些日志保存。那么我们本节就来讲讲如何实现。

## 常用的错误码

+ `404`：服务器没有指定的url。
+ `403`：没有权限访问相关的数据。
+ `405`：请求的 `method`错误。
* `400`：`bad request`，请求的参数错误。
* `500`：服务器内部错误，一般是代码出bug了。
- `502`：一般部署的时候见得比较多，一般是 nginx 启动了，然后 uwsgi 有问题。


## 自定义错误模板

在碰到比如 `404`， `500`错误的时候，想要返回自己定义的模板。那么可以直接在 `templates`文件夹下创建相应错误代码的 `html`模板文件。那么以后在发生相应错误后，会将指定的模板返回回去。

## 错误处理的解决方案

对于 `404`和 `500`这种自动抛出的错误。我们可以直接在 `templates`文件夹下新建相应错误代码的模板文件。而对于其他的错误，我们可以专门定义一个 `app`，用来处理这些错误。
```python
    from django.shortcuts import render
    
    def view_403(request):
        return render(request,'errors/403.html',status=403)
        
    def view_400(request):
        return render(request,'errors/400.html',status=400)
```