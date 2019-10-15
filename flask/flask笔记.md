# FlaskNotes

Flask Nots

## 第一章： Flask入门

### 1.1 URL详解

URL是Uniform Resource Locator的简写，统一资源定位符

```python
scheme://host:post/path/?query-string=xxx#anchor
```

- scheme: 代表的是访问的协议，一般为HTTP或者HTTPS以及tfp等
- host: 主机名、域名，比如：www.baidu.com
- post: 端口号，当你访问一个网站的时候，浏览器默认使用80端口。
- path: 查找路径，比如：www.jianshu.com/trending/now, 后面的trending/now就是路径
- ？query-string: 查询字符串，比如：www.baidu.com/?wd=python, 后面的wd=python就是查询字符串
- anchor: 锚点，后台一般不用管，前段用来做页面的定位，比如：www.baidu.com/item/xxx/xxx?fr=XXX#7

### 1.2 Flask简介

Flask是一个非常流行的python web框架，出生于2010年，作者是Armin Ronacher, 本来这个项目只是作者愚人节的一个玩笑，后来由于非常受欢迎，进而成为一个正式的项目。

Flask自2010年发布第一版依赖，大受欢迎，深受开发者的喜爱，并且在多个公司已经得到了应用。Flask能够如此流行的原因，可以分为以下几点：

- 微框架，简洁，只做他需要做的，给开发者提供了很大的扩展性。
- Flask和相关的依赖设计的非常优秀，用起来很爽
- 开发效率非常高，比如：SQLAlchemy的ORM操作数据库可以节省大量书写sql的时间。
- 社会活跃度非常高

Flask的灵活度非常之高，他不会帮你做太多的决策，即使已经帮你做出了选择，你也能非常用以更换成你需要的，比如：

- 使用Flask开发数据库时，具体使用SQLAlchemy 还是MogoEngine或者是不用ORM而是直接基于MYSQL-Pyton这样的底层驱动进行开发都是可以的。选择权完全掌握在你自己的手中，区别于Django， Django内置了非常完善和丰富的功能，并且加入如果你想替换成你自己想要的，要么不支持，要么非常麻烦。
- 把默认的Jinjia2模板引擎替换成Mako引擎或者是其他模板引擎是非常容易的。

### 1.3 第一个Flask程序

```python
    #!/usr/bin/env python
    # -*- encoding: utf-8 -*-
    '''
    @File    :   app.py
    @Time    :   2019/04/13 08:46:32
    @Author  :   WM
    @Version :   1.0
    @License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
    @Desc    :   None
    '''
    # 从flask这个包中导入Flask类
    # Flask这个类是项目的核心，以后很多操作都是基于这个类的对象
    # 注册url，注册蓝图等都是基于这个类的对象
    from flask import Flask, render_template

    #创建一个Flask对象，传递一个__name__参数进去
    #__name__参数的作用：
    #1. 可以规定模板和静态文件的查找路径
    #2. 以后一些Flask插件，比如Flask-migrate、Flask-SQLAlchemy如果报错了，那么flask
    #可以通过这个参数找到具体的报错位置
    app = Flask(__name__)

    app.config.update({
        # 开启debug模式，方便查看错误
        "DEBUG": True,
        # 开启自动加载模式，修改静态资源后，无需重启，自动加载最新静态资源。
        "TEMPLATES_AUTO_RELOAD": True
    })

    # @app.route('/') 是一个装饰器
    # @app.route('/') 就是将url中的/映射到index这个视图函数上面
    # 以后你访问我这个网站的/目录的时候，会执行index这个函数，然后将这个函数的返回值返回给浏览器
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/my_list/')
    def my_list():
        return 'My list'


    # 如果这个文件作为主文件运行，那么就执行app.run()方法
    # 也就是启动这个网站
    if __name__=='__main__':
    app.run()

```

## 第二章：Flask URL

### 2.1 Debug模式

#### 2.1.1 为什么需要开启debug模式：

1. 如果开启了debug模式， 那么在代码中如果抛出了异常，在浏览器的页面中可以看到具体的错误信息，以及具体的错误代码位置。方便开发者调试
2. 如果开启了debug模式，那么以后再`Python`代码中修改了任何代码，只要按住 `ctrl + s`， `flask`就会自动的重新加载整个网站，不需要手动点击重新运行。

#### 2.1.2 配置debug模式的四中方式

1. 在 `app.run()`中传递一个参数`debug=True`就可以打开`debug`模式。
2. 给`app.debug=True`,也可以开启`debug`模式
3. 通过配置参数的形式设置debug模式，`app.config.update(DEBUG=True)`
4. 通过配置参数的形式设置debug模式，`app.config.from_object(config)`

#### 2.1.3 pin码

如果想要在网页上调试代码，那么应该输入`pin`码。

### 2.2 config 配置文件

#### 2.2.1 使用`app.config.from_object`的方式加载配置文件

1. 导入`import config`。
2. 使用`app.config.from_object(config)`

#### 2.2.2 使用`app.config.from_pyfile`的方式加载配置文件

这种方式不需要`import`，直接使用`app.config.from_pyfile('config.py')`就可以了。
> 注意：这个地方必须要写文件的全名，后缀不能少。

1. 这种方式，加载配置文件，不局限于使用 `py`文件，普通的`txt`文件同样也适合
2. 这种方式可以传递 `silent=True`， 那么静态文件没有找到的时候不会抛出异常。

### 2.3 URL与试图函数映射

#### 2.3.1 传递参数

传递参数的语法是：`/<参数名>/`，然后在试图函数中，也要定义同名的参数

#### 2.3.2 参数的数据类型

1. 如果没有指定具体的数据类型，那么默认就是使用 `string` 数据类型
2. `int` 数据类型只能传递`int`类型
3. `float` 数据类型只能传递`float`类型
4. `path` 数据类型和`string`有点类似，都是可以接受任意的字符串，但是 `path`可以接受路径，也就是说可以包含斜杠。
5. `uuid` 数据类型只能接受符合 `uuid`的字符串。 `uuid`是一个全宇宙都唯一的字符串。一般可以用来做表的主键
6. `any`数据类型可以在一个URL中指定多个路径，

```python
@app.route('/<any(blog, user):url_path>/<id>')
def detail(url_path, id):
    if url_path == 'blog':
        return 'blog detail'
    else:
        return 'user detail'
```

#### 2.3.3 接收用户传递参数的方式

1. 第一种，就是上面讲的方式（将参数嵌入到路径中）;`优势：方便搜索引`擎抓取
2. 第二种，就是使用查询的方式，就是通过`?key=value`的形式传递的。

```python
@app.route('/d/')
def d():
    wd = request.args.get('wd')
    return "您传递的参数是{}".format(wd)
```

1. 如果你的页面想要做`SEO`优化，就是被搜索引擎搜索到，那么就推荐使用第一种方式（path的方式），如果不在乎搜索引擎优化，那么就可以使用第二种。（查询字符串的方式）

### 2.4 url_for URL转换器

#### 2.4.1 基本使用

`url_for`第一个参数，应该是试图函数的名字的字符串，后面的参数就是传递给URL。如果传递的参数之前在 URL 中已经定义了，那么这个参数就会被当成 path 的形式给 URL ，如果这个参数之前没有在 URL 中定义，那么奖变成查询字符串的形式放到 URL 中。

```python
    @app.route('/list/<page>/')
    def my_list(page):
        return 'my_list'
    print(url_for('my_list', page=1, count=2))
    # 构建出来的URL：/my_list/1/?count=2
```

#### 2.4.2 为什么需要url_for

1. 将来如果修改了 URL ，但没有修改该 URL 对应的函数名， 就不用到处去替换 URL 了
2. url_for 会自动的处理那些特殊的字符，不需要手动处理。

```python
    url = url_for('login', next='/')
    # 会自动的将/编码，不需要手动去处理
    # url: /login/?next=%2F
```

> 强烈建议以后再使用URL的时候，使用url_for来反转URL。

#### 2.4.3 自定义URL转换器

##### 2.4.3.1自定义URL转换器的方式

1. 导入`from werkzeug.routing import BaseConverter` 实现一个类，继承自`BaseConverter`
2. 在自定义的类中，重写 `regex`， 也就是这个变量的正则表达式
3. 将自定义的类，映射到`app.url_map.converters`上。例如：

```python
    class TelephoneConverter(BaseConverter):
        # 一个URL中含有手机号码的变量，必须先定这个变量格式满足手机号码的格式
        regex = r'1[85734]\d{9}'
    # 把写好的参数类型注册到converters中
    app.url_map.converters['tel'] = TelephoneConverter
```

##### 2.4.3.2 `to_python`的作用

会将URL中的参数经过解析后传递给视图函数。这个方法的返回值，将会传递到view中作为参数

##### 2.4.3.3 `to_url`的作用

这个方法的返回值，会将在调用url_for函数的时候生成符合要求的URL形式。

#### 2.4.4 必会的小细节知识点

url_detall.py

##### 2.4.4.1 在局域网让其他电脑访问我的网站

如果在一个局域网下的其他电脑访问自己电脑上的Flask网站，那么可以设置 `host='0.0.0.0'`才能访问到。

##### 2.4.4.2 指定端口号

Flask 默认使用5000端口，如果想更换端口，那么可以设置`post=9000`.

##### 2.4.4.3 URL唯一

在定义URL的时候，一定要记得在最后加一个斜杠

1. 如果不加斜杠，那么在浏览器中访问这个URL的时候，如果最后加了斜杠，那么就访问不到，这样用户体验不好
2. 搜索引擎会将不加斜杠的和加斜杠的视为两个不同的URL，而其实加和不加斜杠的都是同一个URL， 那么就会给搜索引擎造成一个误解，加了斜杠，就不会出现没有斜杠的情况。

##### 2.4.4.4 get请求和post请求

在网络请求中有许多请求方式，比如：`get`、`post`、`delete`、`put`请求等，最常用的就是 `get` 和 `]` 请求。

1. `get` 请求：只会在服务器上获取资源，不会更改服务器的状态，这种方式推荐使用get请求。
2. `post`请求： 会给服务器提交一些数据或文件，一般post请求是会对服务器的状态产生影响，那么这种请求推荐使用post请求。
3. 关于传参方式
   1. `get`：把参数请求放到URL中，通过`?xxx=xxx`的形式传输的。
   2. `post`：会把参数放到`Form Data`中。
4. 在`Flask`中，`route`方法，默认将只能使用 get 的方式请求这个URL， 如果想要设置自己的请求方式，那么应该传递一个 `methods` 参数

### 2.5 页面跳转和重定向

重定向分为永久性重定向和暂时性重定向，在页面上体现的操作就是浏览器会从一个页面自动跳转到另外一个页面。比如用户访问了一个需要权限的页面，但是该用户当前并没有登录，因此我们应该给他重定向到登录页面。

- 永久性重定向：HTTP 的状态码是 301， 多用于旧网站被废弃了要转到一个新的网址确保用户访问。
- 暂时性重定向：HTTP 的状态码是 302， 表示页面的暂时性跳转。比如访问一个需要权限的网站，如果当前用户没有登录，应该重定向到登录页面，这种情况下，应该使用暂时性重定向。
  
在Flask中，重定向是通过 `flask.redirect(location, code=302)`这个函数来实现，`location`表示要重定向到的URL， 应该配合之前讲的 `url_for()` 函数来使用， code 表示采用了那个重定向，默认是302 既暂时性重定向，可以修改为301来实现永久性重定向。

```python
from flask import Flask,redirect, request, url_for


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():

    return "hello index"

@app.route('/login/')
def login():

    return 'login Page'

@app.route('/profile/')
def profile():

    if request.args.get('name'):
        return '欢迎来到个人中心'
    else:
        # return redirect("/login/")
        return redirect(url_for('login'), code=302)

if __name__ == '__main__':
    app.run()
```

### 2.6 关于响应(Response)

试图函数的返回值会被自动转换为一个响应对象，Flask的转换逻辑如下：

- 如果返回的是一个合法的响应对象，则直接返回。「其实底层将这个字符串包装成了一个 `Response`对象。」
- 如果返回的是一个字符串， 那么Flask会重新创建一个`werkzeug.wrappers.Response`对象， Response将该字符串作为主体，状态码为200， MIME类型为：text/html， 然后返回Response对象。
- 如果返回的是一个元组，元组中的数据类型是(response.status.headers).status值会覆盖默认的200状态码， headers可以是一个列表或字典，作为额外的消息头。「元组的形式是(响应体,状态码, 头部信息)，也不一定三个都要，写两个也是可以的。返回的元组，在底层也是包装成了`Response`对象」
- 如果以上条件都不满足，Flask会假设返回值是一个合法的`wsgi`应用程序，并通过 `Response.force_type(rv, request.environ)`转换为一个请求对象。

#### 2.6.1 直接用Response创建

```python
from werkzeng.wrappers import Response

@app.route('/')
def index():
    resp = Response(response='about page', status=200, content_type='text/html;charset=utf-8')
    return resp

```

#### 自定义响应

- 必须继承自 Response类。
- 必须实现force_type(cls,rv,environ=None)
- 必须制定app.response_class 为你自定义的Response

```python
    #!/usr/bin/env python
    # encoding: utf-8
    '''
    flask = werkzeng + sqlalchemy + jinja2
    '''

    from flask import Flask, Response, jsonify
    # from werkzeug.wrappers import Response


    app = Flask(__name__)
    app.debug = True


    # 将视图函数中返回字典，转换成json对象然后返回
    # restful-api


    class JsonReponse(Response):
        @classmethod
        def force_type(cls, response, environ=None):
            '''
            这个方法只有视图函数返回非字符串、元组、Response对象，才会调用。
            '''
            # print(response)
            # print(type(response))
            if isinstance(response, dict):
                # jsonify 除了将字典转换为json对象，还将该对象包装成了一个Response对象。
                response = jsonify(response)
            return super(JsonReponse, cls).force_type(response, environ)
            # return Response('hello')


    app.response_class = JsonReponse

    @app.route('/')
    def index():

        # Response("hello world", status=200, mimetype="text/html")
        return 'holle world !!'

    @app.route('/list1/')
    def list1():

        return 'list1', 200, {'X-NAME': 'zhiliao'}


    @app.route('/list2/')
    def list2():

        return {'username': 'zhiliao', 'age': 18}

    @app.route('/list3/')
    def list3():
        # 这种方法可以设置cookie
        res = Response('hello')
        res.set_cookie('country', 'china')
        return res


    if __name__ == '__main__':
        app.run()

```

## 第三章：模板 templates

### 3.1 模板预热

1. 在渲染模板的时候，默认会从项目目录下的 `templates`目录下查找模板。
2. 如果不想把模板文件放在`templates`目录下，可以在Flask初始化的时候指定`template_folder`的路径，来指定模板的路径

### 3.2 模板传参

1. 在使用`render_template`渲染模板的时候，可以传递关键字参数，以后直接在模板中使用就可以了
2. 如果你的参数过多，那么可以将所有的参数放到一个字典中，然后在传这个字典参数的时候，使用两个星号，将字典打散成关键字参数。

### 3.3 模板中使用url_for

模板中的`url_for`跟我们后台视图函数中的 `url_for`使用起来基本是一模一样的，也是传递视图函数的名字，也可以传递参数。使用的时候，需要在`url_for`左右加上花括号`{{ url_for }}`

### 3.4 模板中过滤器基本是使用

回到我们第一篇开篇的例子，我们在模板中对变量name作如下处理：
`<h1>Hello {{ name | upper }}!</h1>`
你会看到name的输出都变成大写了。这就是过滤器，只需在待过滤的变量后面加上”|”符号，再加上过滤器名称，就可以对该变量作过滤转换。上面例子就是转换成全大写字母。过滤器可以连续使用：
`<h1>Hello {{ name | upper | truncate(3, True) }}!</h1>`
现在name变量不但被转换为大写，而且当它的长度大于3后，只显示前3个字符，后面默认用”…”显示。过滤器”truncate”有3个参数，第一个是字符截取长度；第二个决定是否保留截取后的子串，默认是False，也就是当字符大于3后，只显示”…”，截取部分也不出现；第三个是省略符号，默认是”…”。

其实从例子中我们可以猜到，过滤器本质上就是一个转换函数，它的第一个参数就是待过滤的变量，在模板中使用时可以省略去。如果它有第二个参数，模板中就必须传进去。

过滤器是通过管道符号(|)进行使用的，例如`{{ name | length}}`,将返回name的长度。过滤器相当于是一个函数，把当前的变量传入到过滤器中，然后获取器根据自己的功能，返回相应的值，之后再将结果渲染到页面，Jinja2中内置了很多过滤器，现在对一些常用的过滤器进行讲解

#### 3.4.1 字符串操作

```jinja
{# 当变量未定义时，显示默认字符串，可以缩写为d #}
<p>{{ name | default('No name', true) }}</p>

{# 单词首字母大写 #}
<p>{{ 'hello' | capitalize }}</p>

{# 单词全小写 #}
<p>{{ 'XML' | lower }}</p>

{# 去除字符串前后的空白字符 #}
<p>{{ '  hello  ' | trim }}</p>

{# 字符串反转，返回"olleh" #}
<p>{{ 'hello' | reverse }}</p>

{# 格式化输出，返回"Number is 2" #}
<p>{{ '%s is %d' | format("Number", 2) }}</p>

{# 关闭HTML自动转义 #}
<p>{{ '<em>name</em>' | safe }}</p>

{% autoescape false %}
{# HTML转义，即使autoescape关了也转义，可以缩写为e #}
<p>{{ '<em>name</em>' | escape }}</p>
{% endautoescape %}
```

#### 3.4.2 数值操作

```html
{# 四舍五入取整，返回13.0 #}
<p>{{ 12.8888 | round }}</p>

{# 向下截取到小数点后2位，返回12.88 #}
<p>{{ 12.8888 | round(2, 'floor') }}</p>

{# 绝对值，返回12 #}
<p>{{ -12 | abs }}</p>
```

#### 3.4.3 列表操作

```html
{# 取第一个元素 #}
<p>{{ [1,2,3,4,5] | first }}</p>

{# 取最后一个元素 #}
<p>{{ [1,2,3,4,5] | last }}</p>

{# 返回列表长度，可以写为count #}
<p>{{ [1,2,3,4,5] | length }}</p>

{# 列表求和 #}
<p>{{ [1,2,3,4,5] | sum }}</p>

{# 列表排序，默认为升序 #}
<p>{{ [3,2,1,5,4] | sort }}</p>

{# 合并为字符串，返回"1 | 2 | 3 | 4 | 5" #}
<p>{{ [1,2,3,4,5] | join(' | ') }}</p>

{# 列表中所有元素都全大写。这里可以用upper,lower，但capitalize无效 #}
<p>{{ ['tom','bob','ada'] | upper }}</p>
```

#### 3.4.4 字典列表操作

``` html
{% set users=[{'name':'Tom','gender':'M','age':20},
              {'name':'John','gender':'M','age':18},
              {'name':'Mary','gender':'F','age':24},
              {'name':'Bob','gender':'M','age':31},
              {'name':'Lisa','gender':'F','age':19}]
%}

{# 按指定字段排序，这里设reverse为true使其按降序排 #}
<ul>
{% for user in users | sort(attribute='age', reverse=true) %}
     <li>{{ user.name }}, {{ user.age }}</li>
{% endfor %}
</ul>

{# 列表分组，每组是一个子列表，组名就是分组项的值 #}
<ul>
{% for group in users|groupby('gender') %}
    <li>{{ group.grouper }}<ul>
    {% for user in group.list %}
        <li>{{ user.name }}</li>
    {% endfor %}</ul></li>
{% endfor %}
</ul>

{# 取字典中的某一项组成列表，再将其连接起来 #}
<p>{{ users | map(attribute='name') | join(', ') }}</p>
```

#### 3.4.5 Flask内置过滤器

Flask提供了一个内置过滤器”tojson”，它的作用是将变量输出为JSON字符串。这个在配合Javascript使用时非常有用。我们延用上节字典列表操作中定义的”users”变量

```javascript
<script type="text/javascript">
var users = {{ users | tojson | safe }};
console.log(users[0].name);
</script>
```

#### 3.4.6 自定义过滤器

##### 3.4.6.1 第一种方式(自定义方法)

内置的过滤器不满足需求怎么办？自己写呗。过滤器说白了就是一个函数嘛，我们马上就来写一个。回到Flask应用代码中：

```python
def double_step_filter(l):
    return l[::2]
```

我们定义了一个”double_step_filter”函数，返回输入列表的偶数位元素（第0位，第2位,..）。怎么把它加到模板中当过滤器用呢？Flask应用对象提供了”add_template_filter”方法来帮我们实现。我们加入下面的代码：

```python
app.add_template_filter(double_step_filter, 'double_step')
```

函数的第一个参数是过滤器函数，第二个参数是过滤器名称。然后，我们就可以愉快地在模板中使用这个叫”double_step”的过滤器了：

```python
{# 返回[1,3,5] #}
<p>{{ [1,2,3,4,5] | double_step }}</p>
```

##### 3.4.6.2 第二种方式(装饰器方法)

Flask还提供了添加过滤器的装饰器”template_filter”，使用起来更简单。下面的代码就添加了一个取子列表的过滤器。装饰器的参数定义了该过滤器的名称”sub”。 例子:`template_app.py`  and  `filter.html`;

```python
@app.template_filter('sub')
def sub(l, start, end):
    return l[start:end]
```

我们在模板中可以这样使用它：

```python
{# 返回[2,3,4] #}
<p>{{ [1,2,3,4,5] | sub(1,4) }}</p>
```

Flask添加过滤器的方法实际上是封装了对Jinja2环境变量的操作。上述添加”sub”过滤器的方法，等同于下面的代码。

```python
app.jinja_env.filters['sub'] = sub
```

我们在Flask应用中，不建议直接访问Jinja2的环境变量。如果离开Flask环境直接使用Jinja2的话，就可以通过”jinja2.Environment”来获取环境变量，并添加过滤器。

### 3.5 逻辑处理（if、for）

#### 3.5.1 if语句

if 条件判断语句，必须放在 {% if statement %} 中间，并且必须有结束语句 `{% endif %}` 。和`Python`中的类似，可以使用 `<、 >、 <=、 >=、 !=`来进行判断，也可以通过 `and、 or、 not、 （）`来进行逻辑合并处理。

#### 3.5.2 for循环

在 `Jinjia2` 中的 `for` 循环，跟 `Python` 中的 `for` 循环基本上一模一样，也是 `for...in...` 的形式，并且可以遍历所有的序列以及迭代器。但是唯一不同的是， `Jinjia2` 中的 `for` 循环没有 `continue` 和 `break` 语句。

`jinjia` 中的 `for` 循环还包含以下变量，可以用来获取当前的遍历状态。
变量|描述
--|--
loop.index| 当前迭代的索引，从1开始
loop.index0| 当前迭代的索引，从0开始
loop.first| 是否是第一次迭代，返回True或False
loop.last| 是否是最后一次迭代，返回True或False
loop.length| 序列的长度

另：不可以使用`continue` 和 `break`表达式来控制循环的执行。

### 3.6 宏 和 import 语句 include 语句

模板中的宏跟Python中的函数类似，可以传递参数，但是不能有返回值，可以将一些经常用到的代码片段放到宏中，然后把一些不固定的值抽取出来当成一个变量。
使用宏的时候，参数可以为默认值。

定义宏

``` html
{% macro input(name="", value="", type="") %}
    <input type="{{ type }}" name="{{ name }}" value="{{ value }}">
{% endmacro %}
```

使用宏

``` html
<table>
    <tbody>
        <tr>
            <td>用户名:</td>
            <td>{{ input('username') }}</td>
        </tr>
        <tr>
            <td>密码:</td>
            <td>{{ input('password', type="password") }}</td>
        </tr>
        <tr>
            <td></td>
            <td>{{ input(value="提交", type="submit") }}</td>
        </tr>
    </tbody>
</table>
```

#### 3.6.1 import 宏

flask中 导入宏是从 templates 中开始计算路径

1. import "宏文件路径" as 'xxx'
2. from "宏文件的路径" import 宏的名字 [as xxx]
3. 宏文件的路径，不要以相对路径去寻找，都要以`templates`最为绝对路径去查找。
4. 如果想要在导入宏的时候，就把当前模板的一些参数传给宏所在的模板中，那么久应该在导入的时候使用 `with context`。实例：`from 'xxx.html' import input with context`

```html
# 第一种导入方式
{% from "macro_base.html" import input %}

# 第二种导入方式
# 导入macro_base中所有的宏
# 使用时 需要 macro_base.input() 名称.宏名称
{% import "macro_base.html" as macro_base %}

```

#### 3.6.2 include

1. 这个标签相当于是直接将指定的模板中的代码复制粘贴到当前位置。
2. include 如果想要使用覆膜板中的变量，直接用就可以了， 不需要使用with context
3. include 的路径，也是跟 import一样， 直接从templates跟目录下去找，不要以相对路径去找。

### 3.7 设置变量、加载静态文件、继承

#### 3.7.1 set、with及模板中定义变量

##### 3.7.1.1 set with 语句

在模板中，可以使用`set`语句来定义变量，一旦定义了变量，那么在后面的代码中，都可以使用这个变量，就类似于Python的变量定义是一样的。

```html
{%set username='alex'%}
<p>用户名{{ username }}</p>
```

`with` 语句定义的变量，只能在 `with` 语句块中使用，超过了这个代码块，就不能再使用了。 `with` 中使用 `set` 定义了变量，超出 `with` 块后也是不能使用的。

```html
{% with classroom = '一年级三班' %}
    <p>班级：{{ classroom }}</p>
{% encwith%}
```

#### 3.7.2 加载静态文件

```css
<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css')}}">
```

#### 3.7.3 模板继承

1. 为什么需要模板继承
    1. 模板继承可以把一些公用的代码单独抽取出来放到一个父模板中，以后子模板直接继承就可以使用了，这样可以重复性的代码，以后修改起来比较方便。
2. 模板继承语法
    1. 使用 `extends`语句，来指明继承的父模板，父模板的路径，也是相对于templates文件夹下的绝对路径。
    2. `{% extends 'base.html' %}`
3. block语法
    1. 一般在父模板中，定义一些公用的代码，子模板可能要根据具体的需求实现不同的代码，这时候父模板就应该有能力提供一个接口，让父模板来实现，从而实现具体业务需求的功能。

4. 调用另外一个block中的代码

    如果想要在另外一个模板中使用其他模板中的代码，那么可以通过 `{{ self.其他block名字() }}`就可以了。示例代码如下：

    ```html
    {% block title %}
        标题
    {%endblock%}

    {% block body_block %}
        {{ self.title() }}
        <p>代码</p>
    {% endblock body_block %}
    ```

5. 其他注意事项
    1. 子模板中的代码，第一行，应该是 `extends`
    2. 子模板中，如果要实现自己的代码，应该放到block中，如果放到其他地方，那么久不会被渲染

在父模板定义入口

```html
{% block body_block %}

{% endblock body_block %}
```

在子模板中调用

```html
{% extends 'inherit/base.html' %}
{% block body_block %}
    <div>
        我是首页
    </div>
{% endblock body_block %}
```

在子模板中保留父模板中的代码

```html
{% extends 'inherit/base.html' %}
{% block body_block %}
    {{ super() }}
    <div>
        我是首页
    </div>
{% endblock body_block %}
```

## 第四章： 视图高级

### 4.1 add_url_rule和approute原理剖析

1. `add_url_rule(rule,endpoint=None, viwe_func=None)` 这个方法用来添加url与视图函数的映射，如果没有填写 `endpoint` ，那么就默认会使用 `view_func` 的名字作为 `endpoint` 。以后再使用 `url_for` 的时候， 就要看在映射的时候有没有传递 `endpoint` 参数，如果传递了，那么就应该使用 `endpoint` 指定的字符串，如果没有传递，那么久应该使用 `view_func` 的名字。

2. `app_route(rule, **options)`装饰器，其实也是使用 `add_url_rule` 来实现 url 与视图函数映射的。

### 4.2 类视图

#### 4.2.1 标准类视图

1. 标准类视图，必须继承自 `flask.views.View`
2. 必须实现 `dipatch_request` 方法，以后求情过来后，都会执行这个方法，这个方法的返回值就相当于之前函数视图一样， 也必须返回 `Response` 或者子类对象，或者是字符串，或者是元祖。
3. 必须通过 `app.add_url_rule(rule, endpoint, view_func)` 来做url与视图的映射。 `view_func` 这个参数，需要使用类视图下的 `as_view` 类方法类转换， `ListView.as_view('list')`
4. 如果指定了 `endpoint` ，那么在使用 `url_for` 反转的时候就必须使用 `endpoint` 指定的那个值， 如果没有指定 `endpoint` ，那么久可以直接使用 `as_view(视图名字)` 来指定的属兔名字来作为反转。
5. 视图类有一下好处：可以继承，把一些共性的东西抽取出来放到父类视图中，子类视图直接拿来用就可以了，但是也不是说所有的视图都要使用类视图，这个要根据情况而定。

#### 4.2.2 基于方法的类视图

1. 基于方法的类视图，是根据请求的 `method` 来执行不同的方法。如果用户发的是 `get` 请求，那么将会执行这个类的 `get` 方法。如果用户发的是 `post` 请求，那么将会执行 `post` 方法。其他 `method` 请求类型，例如 `delete` `put` 等。
2. 这种方式，可以让代码更加简洁。所有的 `get` 请求相关的代码都放到 `get` 方法中。所有 `post` 请求相关的代码都放到 `post` 方法中。

#### 4.2.3类视图中的装饰器

1. 如果使用的是函数视图，那么自定义的装饰器必须放在 app_route 下面。否则这个装饰器就起不到任何作用
2. 类视图的装饰器，需要重写类视图的一个类属性 decorators ，这个类属性是一个列表或者元祖都可以。里面装的就是所有的装饰器。

### 4.3 蓝图 BluePrint

- 蓝图的作用就是让我们的flask项目更加模块化，结构更加清晰。可将相同模块的视图函数放在同一个蓝图下，同一个文件中，方便管理。
- 基本语法

    ~ 在蓝图文件中导入蓝图，

    ```python
    from flask import Blueprint
    user_bp = Blueprint('user', __name__)
    ```

    ~ 在APP文件中注册蓝图

    ```python
    from blueprint.user import user_bp
    app.regist_blueprint(user_bp)
    ```

- 如果想要某个蓝图下的所有url都有一个url前缀，那么可以在定义蓝图的时候，指定 `url_prefix` 参数

    ```python
    user_bp = Blueprint('user', __name__, url_prefix='/user')
    ```

在定义 `url_prefix` 的时候，要注意后面的 斜杠，如果给了那么以后再定义url时，就不要在全面加斜杠。

- 蓝图模板文件的查找：
    ~ 如果项目中的 templates 文件夹中有相应的模板文件，就直接使用了。
    ~ 如果项目中的 templates 文件夹中没有相应的模板文件，那么就到在定义蓝图的时候指定的路径中寻找。并且蓝图中指定的路径可以为相对路径，相对的是当前这个蓝图文件所在的目录。比如：

    ```python
    news_bp =  Blueprints('news', __name__, url_prefix='/news', template_folder='zhiliao')
    ```

    因为这个蓝图文件是在 blueprints/news.py，那么就会到 blueprints这个文件夹下的 zhiliao 文件夹中寻找模板文件。

- 蓝图中静态文件的查找规则：
    ~ 在模板文件中，加载静态文件，如果使用 url_for('static'), 那么就会在APP指定的静态文件夹目录下查找静态文件。
    ~ 如果在加载静态文件的时候，指定了蓝图的名字，比如 news.static , 那么就会到这个蓝图指定的static_folder下查找静态文件。
- url_for 翻转蓝图中的视图函数为URL：
    如果使用蓝图，那么以后想要翻转蓝图中的视图函数为URL，那么就应该在使用url_for 的时候指定这个蓝图。比如 news.news_list。否则就找不到这个 endpoint 。在模板中的url_for 同样也是要满足这个条件，就是指定蓝图的名字。

#### 4.4 蓝图实现子域名

1. 使用蓝图技术。
2. 在创建蓝图对象的时候，需要传递一个 subdomain 参数， 来指定这个子域名的前缀，例如： cms_bp = Blueprint('cms', __name__, subdomain='cms').
3. 需要在APP文件中， 配置 app.config 的 SERVER_NAME 参数。例如：

    ```python
    app.config['SERVER_NAME'] = 'jd.com:5000'
    ```

    - ip 地址不能有子域名
    - localhost 不能有子域名
4. 要修改host, 添加域名与本机的映射。子域名也需要做映射。

    ```python
    127.0.0.1  jd.com
    127.0.0.1  cms.jd.com
    ```

## 第五章： 数据库

### 5.1 Mysql 数据库安装

### 5.2 SQLAlchemy 介绍和基本使用

#### 5.2.1 依赖

1. 安装MySQL
2. 安装 MySQLdb：MySQLdb是用来操作MySQL的包，可以通过pip来安装 `pip install mysql-python` | `python2`
3. 安装 pymysql：pymysql是用来操作MySQL的包，可以通过pip来安装 `pip install pymysql` | `python3`
4. SQLAlchemy: SQLAlchemy是一个数据库的orm框架，我们在后面会用到，可以通过pip 来安装 `pip install SQLAlchemy`

#### 5.2.2 使用SQLAlchemy

1. 连接数据库

使用SQLAlchemy去连接数据库，需要使用一些配置信息，然后将他们组合成满足条件的字符串；

```python
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'first_sqlalchemy'
USERNAME = 'root'
PASSWORD = 'root'
DB_URL = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE
)

```

然后使用 create_engine 创建一个引擎 engine ， 然后在调用这个引擎的 connect 方法，就可以得到这个对象，然后就可以通过这个对象对数据库进行操作了

```python
# 连接sqlite3
# 相对路径连接数据库
db_con = create_engine('sqlite:///test.db?check_same_thread=False', echo=True)

engine = create_engine(DB_URL)
# 判断是否连接成功
conn = engine.connect()
conn.execute('select 1')
```

#### 5.2.3 SQLAlchemy ORM(object relationship mapping)

模型对象与数据库表的映射

##### 5.2.3.1 将ORM模型映射到数据库中：

1. 用 declarative_base 根据 engine 创建一个ORM基类

   ```python
   from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine('sqlite:///ceshi.db?check_same_thread=False', echo=True)
    Base = declarative_base(engine)
   ```

2. 用这个 Base 类作为基类来写自己的ORM类，要定义`__tablename__`类属性，来指定这个模型映射到数据库中的表名。

   ```python
   class Person(Base):
       __tablename__ = 'person'
   ```

3. 创建属性来映射到表中的字段，所有需要映射到表中的属性都应该为`Column`类型：

   ```python
   class Person(Base):
        __tablename__ = 'person'  # 定义表的名字

        # 2.在这个ORM模型中创建一些属性，来跟表中的字段进行一一映射，这些属性必须是 sqlalchemy 给我们提供好的数据类型
        id = Column(Integer, primary_key=True, autoincrement=True)   # 定义列？
        name = Column(String(50))
        age = Column(Integer)
   ```

4. 使用 `Base.metadata.create_all()`来将模型映射到数据库中。
5. 一旦使用了`Base.metadata.create_all()`将模型映射到模型后，即使改版了模型的字段，也不会重新映射了。

### 5.3 SQLAlchemy 常用类型及参数

#### 常用类型

1. Integer：  整形
2. Float： 浮点类型
3. Boolean： 传递True/False
4. BECIMAL： 定点类型，解决Float精度丢失问题，这个参数只用的时候需要传递两个参数，第一个参数是用来标记这个字段总共能存储多少个数字，第二个参数表示小数点后有多少位。
5. Enum： 枚举类型,指定某个字段只能是枚举中指定的几个值，不能为其他值。在ORM模型中，使用Enum 来作为枚举，实例如下

   ```python
    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer, primary_kdy=True, autoincrement=True)
        tag = Column(Enum('python', 'flask', 'django'))
   ```

   在Python3中， 已经内置了 enum这个模块，我们也可以使用这个模块定义相关的字段，实例如下

   ```python
    class TagEnum(enum.Enum):
        python = 'python'
        flask = 'flask'
        django = 'django'

    class Article(Base):
        __tablename__ = 'article'
        id = Column(Integer, primary_kdy=True, autoincrement=True)
        tag = Column(Enum(TagEnum))

    article = Article(tag=TagEnum.python)
   ```

6. Date： 存储时间，只能存储年 月 日， 映射到数据库中是date类型。在Python代码中， 可以使用datetime.date来指定。实例代码如下：

   ```python
    class Article(Base):
        # 创建数据库表名称
        __tablename__ = 'article'
        id = Column(Integer, primary_key=True, autoincrement=True)
        # date 类型
        create_date = Column(Date)

    from datetime import date
    article = Article(create_date=date(2019, 5, 29))

   ```

7. DateTime：可以存储 年 月 日 时  分 秒 毫秒等，映射到数据库中也是datetime类型。在Python代码中，可以使用 datetime.datetime 来指定。实例代码如下：

   ```python
    class Article(Base):
        # 创建数据库表名称
        __tablename__ = 'article'
        id = Column(Integer, primary_key=True, autoincrement=True)
        # date 类型
        create_date = Column(DateTime)

    from datetime import datetime
    article = Article(create_date=datetime(2019, 5, 29, 11, 11, 11))
   ```

8. Time： 存储时间可以存储时 分 秒， 映射到数据库中也是time类型。在Python代码中，可以使用datetime.time 来指定，实例代码：

   ```python
   class Article(Base):
        # 创建数据库表名称
        __tablename__ = 'article'
        id = Column(Integer, primary_key=True, autoincrement=True)
        # date 类型
        time = Column(Time)

    from datetime import time
    article = Article(create_date=time(hour=11, minute=11, second=11))
   ```

9. String： 字符串类型，使用时需要制定长度，区别于Text类型
10. Text： 文本类型
11. LONGTEXT： 只有MySQL中存在 需要在 from sqlalchemy.dialects.mysql import LONGTEXT 中导入。

#### 常用参数

1. primary_key： 设置某个字段为主键
2. autoincrement： 设置字段自增长
3. default： 设置某个字段的默认值。
4. nullable： 指定某个字段是否可以为空，nullable=True 可以为空，nullable=False 不能为空。
5. unique： 指定某个字段是否为空，默认是False（默认可以重复）
6. onupdate： 在数据更新的时候，会调用这个参数指定的值或参数，在第一次插入这条数据的时候，不会用onupdate的值，只会用default的值。常用的就是 update_time (每次更新数据的时候都要更新的值)。
7. name： 指定ORM中某个属性映射到表中的字段名，如果不指定，那么就会使用这个属性的名字来作为字段名，如果指定了，就会使用指定的这个值作为参数，这个参数也可以当做位置参数，在第一个参数来指定。

   ```python
    title = Column(String(50), name="my_title")
    title = Column("my_title", String(50))
   ```

#### query可用参数

1. 模型对象。指定查找这个模型中所有的对象
2. 模型中的属性，可以指定只查找某个模型的其中几个属性。
3. 聚合函数
   1. func.count： 统计行的数量
   2. func.avg： 求平均值
   3. func.max： 求最大值
   4. func.min： 求最小值
   5. func.sum： 求和。
   func 上，其实没有任何聚合函数，但是因为他底层实现了一些魔术方法，只要MySQL中有的聚合函数，都可以通过func来调用。

#### filter 过滤条件

过滤是数据提取的一个很重要的功能， 以下对一些常用的过滤条件进行解释，并且通过这些过滤条件都是只能通过filter方法实现的。

1. equal:

    ```python
    art  = sesson.query(Article).filter(Article.title == 'title0').first()
    print(art)
    ```

2. not  equal

    ```python
    art = sesson.query(Article).filter(Article.title != 'title0').all()
    print(art)
    ```

3. like 模糊查询 ilike  不区分大小写

    ```python
    art = sesson.query(Article).filter(Article.title.like('title%')).all()
    print(art)
    ```

4. in

    ```python
    art = sesson.query(Article).filter(Article.title.in_(['title1', 'title2'])).all()
    print(art)
    ```

5. not in 两种实现方式. < ~ >

    ```python
    art = sesson.query(Article).filter(Article.title.notin_(['title1', 'title2', 'title3'])).all()
    print(art)
    art = sesson.query(Article).filter(~Article.title.in_(['title1', 'title2', 'title3'])).all()
    print(art)
    ```

6. is null | is not null

    ```python
    art = sesson.query(Article).filter(Article.title == None).all()

    ```

7. and

    ```python
    art = sesson.query(Article).filter(and_(Article.title='title01', Article.id=5)).all()
    ```

8. or

    ```python
    art = sesson.query(Article).filter(or_(Article.title == 'title2', Article.id = 3)).all()
    print(art)
    ```

    如果想要查看ORM底层SQL语句，可以在filter方法后面不要在执行任何方法打印就可以看到了，比如：

    ```python
    art = sesson.query(Article).filter(or_(Article.title == 'title2', Article.id = 3))
    print(art)
    ```

### 5.4 表关系

#### 5.4.1 外键

使用SQLAlchemy 创建外键非常简单，在从表中增加一个字段，指定这个字段外键的是那个表的那个字段就可以了，从表中外键字段，必须和父表的主键字段类型保持一致。

```python

from sqlalchemy import create_engine, Column, Integer, String, Float, func, and_, or_, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

engine = create_engine('sqlite:///test1.db?check_same_thread=False', echo=True)

Base = declarative_base(engine)
sesson = sessionmaker(engine)()


class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    def __repr__(self):
        return "<User(username:{})>".format(self.username)


class Article(Base):
    __tablename__='article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    uid = Column(Integer, ForeignKey("user.id", ondelete='RESTRICT'))

    def __repr__(self):
        return "<Article(title: {}, content: {})>".format(self.title, self.content)

Base.metadata.create_all()

sesson.commit()

```

#### 5.4.2 外键约束 ondelete=”RESTRICT“

1. RESTRICT: 父表数据被删除，会阻止删除，默认就是这一项
2. NO ACTION: 在MySQL中，同 RESTRICT
3. CASCADE: 级联删除
4. SET NULL: 父表数据被删除，字表数据会被设置为NULL

#### 5.4.3 ORM 关系以及一对多

MySQL 级别的外键，还不够 ORM，必须要拿到一个表的外键，然后通过这个外键再去另外一张表中查找，这样太麻烦，SQLAlchemy提供了一个`relationship`，这个类可以定义属性，以后再访问相关关联的表的时候就直接可以通过属性访问的方式就可以访问得到了，示例代码：

```Python
class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    # articles = relationship("Article")

    def __repr__(self):

        return "<User(username: {})>".format(self.username)


class Article(Base):
    __tablename__='article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    uid = Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"))

    author = relationship("User", backref="article")

    def __repr__(self):
        return "<Article(title: {}, content: {})>".format(self.title, self.content)
```

另外可以通过 `backref` 来指定反向访问的属性名称。

#### 5.4.4 一对一关系

在`sqlalchemy`中，如果想要将两个模型映射成一对一关系，那么应该在父模型中，指定引用的时候，要传递一个 `uselist=False` 这个参数进去。就是告诉父模型，以后引用这个从模型的时候，不再是一个对象了。实例代码如下：

```python
class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    # 指定针对 UserExtend 一对一关系。
    extend = relationship('UserExtend', uselist=False)

    def __repr__(self):

        return "<User(username: {})>".format(self.username)


class UserExtend(Base):
    __tablename__='user_extend'
    id = Column(Integer, primary_key=True, autoincrement=True)
    school = Column(String(50), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    # 一对一关系。
    user = relationship("User", backref=backref("extend", uselist=False) )

    def __repr__(self):
        return "<UserExtend(shool: {})>".format(self.school)

```

当然，也可以借助 sqlalchemy.orm.backref 来简化代码：

```python
class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    # articles = relationship("Article")
    # 指定针对 UserExtend 一对一关系。
    # extend = relationship('UserExtend', uselist=False)

    def __repr__(self):

        return "<User(username: {})>".format(self.username)


class UserExtend(Base):
    __tablename__='user_extend'
    id = Column(Integer, primary_key=True, autoincrement=True)
    school = Column(String(50), nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    # 一对一关系。
    user = relationship("User", backref=backref("extend", uselist=False) )

    def __repr__(self):
        return "<UserExtend(shool: {})>".format(self.school)
```

#### 5.4.5 多对多关系

1. 多对多的关系需要一个中间表来绑定他们之间的关系
2. 先把两个需要做多对多的模型定义出来
3. 只用Table定义一个中间表，中间表一般就是包含两个模型的外键字段就可以了， 并且让他们两个来作为一个 复合主键
4. 在两个需要做多对多的模型中随便选择一个模型， 定义一个 relationship 属性，来绑定三者之间的关系，在使用 relationship 的时候，需要传入一个 secondary=中间件。

#### 5.4.6 ORM层面删除数据：

ORM层面删除数据，会无视MySQL级别的外键约束。直接回将对应的数据删除，然后将从表中的那个外键设置null。 如果想要避免这种行为，应该将从表中的外键的 `nullable=Fasle`。

```python
sesson.delete(tags)
```

#### 5.4.8 排序

1. order_by：可以指定根据这个表中的某个字段进行排序， 如果在前面加了一个`-`，代表是降序排序。
2. 在模型定义的时候指定默认排序：有些时候，不想每次都在查询的时候都指定排序的方式，可以在定义模型的时候就指定排序方式。有一下两种方式：
    - relationship 的 order_by参数：在指定relationship的时候，传递order_by参数来指定排序的字段
    - 在模型定义中，添加一下代码：
    '''Python
    __mapper_args = {
        "order_by": titles
    }
    '''
    既可让文章使用标题来进行排序。
3. 正序排序与倒序排序： 默认是正序排序，如果需要使用倒序排序，那么可以使用这个字段的 `desc()`方法，或者是在排序的时候使用这个字段的字符串名字，然后在前面添加一个 `-` 。

#### 5.4.9 limit offset 和切片

1. limit : 可以限制每次查询的时候只查询几条数据。
2. offset : 可以限制查找数据的时候过滤掉前面多少条
3. 切片 : 可以对 query 对象使用切片操作，来获取想要的数据 , 可以使用 slice(start, stop) 方法来做切片操作，也可以使用[start:stop] 的方式来进行切片操作。一般在实际开发中，中括号的相识是用的比较多的。示例代码如下：

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, func, and_, or_, ForeignKey, Text, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import random, datetime

engine = create_engine('sqlite:///test1.db', echo=True)

Base = declarative_base(engine)
session = sessionmaker(engine)()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    create_time = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):

        return "<Article(id: {}, title: {}, create_time: {})>".format(
            self.id, self.title, self.create_time
        )

def test_():
    Base.metadata.drop_all()
    Base.metadata.create_all()


    for x in range(100):
        title = 'title {}'.format(x)
        article = Article(title=title)
        session.add(article)

# article = session.query(Article).all()
# article = session.query(Article).limit(10).all()
# article = session.query(Article).offset(10).limit(10).all()
# article = session.query(Article).order_by(Article.id.desc()).offset(10).limit(10).all()
# article = session.query(Article).order_by(Article.id.desc()).slice(0, 10).all()
article = session.query(Article).order_by(Article.id.desc())[0: 10]
print(article)

session.commit()

```

##### 懒加载

在一对多，或者多对多的时候，如果想要获取多的一部分的数据的时候，往往能通过一个属性就可以全部获取了，比如有一个作者，想要获取这个作者的所有文章，那么就可以通过 user.articles 就可以获取所有的。但有时候我们不想获取所有的数据，比如只想获取作者今天发表的文章，那么这个时候就可以给 relationship 传递一个 lazy='dynamic',以后通过 user.articles 获取到的就不是一个列表，而是一个 AppenderQuery 对象了，这样就可以对这个对象在进行一层过滤和排序操作。
通过 lazy='dynamic' , 获取出来的多的那一部分的数据，就是一个 AppenderQuery 对象了，这种对象既可以添加新数据， 也可以跟 Query 一样，可以再进行一层过滤。
总而言之一句话： 如果你在获取数据的时候，想要在多的那一边的数据再进行一层过滤，那么就可以考虑使用 lazy='dynamic'。

lazy 可用选项：

1. select ： 这个是默认选项，还是拿 user.articles 的例子，如果你没有访问 user.articles 这个属性，那么 sqlalchemy 就不会从数据库中查找文章。 一旦你访问了这个属性， 那么 sqlalchemy 就会立马从数据库中查找所有的文章，并把所有的文章组装成一个列表返回。这也是懒加载。
2. dynamic : 这个就是刚讲的，就是在访问 user.articles 的时候返回回来的不是一个列表， 而是 AppenderQuery 对象。

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, func, and_, or_, ForeignKey, Text, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship, backref
import random, datetime

engine = create_engine('sqlite:///test4.db', echo=True)

Base = declarative_base(engine)
session = sessionmaker(engine)()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)

    def __repr__(self):
        return "<User(id: {}, username: {})>".format(self.id, self.username)


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    uid = Column(Integer, ForeignKey('user.id'))
    # 写在多的一方， 懒加载 lazy='dynamic'
    author = relationship('User', backref=backref('article', lazy='dynamic'))

    def __repr__(self):

        return "<Article(id: {}, title: {}, create_time: {})>".format(
            self.id, self.title, self.create_time
        )

def t4st():
    Base.metadata.drop_all()
    Base.metadata.create_all()


    user = User(username='zhiliao')

    for x in range(100):
        article = Article(title="title {}".format(x))
        article.author = user
        # article 不是一个列表，不能使用append添加数据
        # article.author.append(user)
        session.add(article)

user = session.query(User).first()
# 是一个query对象
# print(user.article)
# print(user.article.filter(Article.id > 50).all())
# 因为是AppendQuery，所以可以继续追加数据进去
articles = Article(title='title 100')
user.article.append(articles)
session.commit()

```

### 5.5 高级查询

#### 5.5.1 group_by

根据某个字段进行分组。比如想要根据性别进行分组，来统计每个分组分别有多少人，那么可以使用一下代码来完成：

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, func, and_, or_, ForeignKey, Text, Table, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship, backref
import random, datetime

engine = create_engine('sqlite:///test4.db', echo=True)

Base = declarative_base(engine)
session = sessionmaker(engine)()


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    age = Column(Integer, default=0)
    gender = Column(Enum('male', 'female', 'secret'), default='male')

    def __repr__(self):
        return "<User(username: {}, age: {}, gender: {})>".format(self.username, self.age, self.gender)

def init_test():
    Base.metadata.drop_all()
    Base.metadata.create_all()


    session.add_all(
        [
            User(username="王武", age= 17, gender='male'),
            User(username="赵柳", age= 17, gender='male'),
            User(username="张三", age= 18, gender='female'),
            User(username="王大武", age= 19, gender='female'),
            User(username="知了", age= 20, gender='female'),
        ]
    )

    session.commit()

# 各年龄段的人数 group_by()
user = session.query(User.age, func.count(User.id)).group_by(User.age).all()
print(user)

```

#### 5.5.2 having

having是对查找结果进一步过滤，比如只想要看未成年人的数量，那么就可以首先对年龄进行分组统计人数，然后在对分组进行having过滤。实例代码如下：

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, func, and_, or_, ForeignKey, Text, Table, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship, backref
import random, datetime

engine = create_engine('sqlite:///test4.db', echo=True)

Base = declarative_base(engine)
session = sessionmaker(engine)()


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    age = Column(Integer, default=0)
    gender = Column(Enum('male', 'female', 'secret'), default='male')

    def __repr__(self):
        return "<User(username: {}, age: {}, gender: {})>".format(self.username, self.age, self.gender)

# having
user = session.query(User.age, func.count(User.id)).group_by(User.age).having(User.age < 18).all()
print(user)

```

#### 5.5.3 join

1. left join 左外链接
2. right join 右外链接
3. inner join 内链接

> SELECT * FROM a LEFT JOIN b on a.id=b.id 左外链接

内链接

> SELECT * FROM a INNER JOIN b on a.id=b.id 内链接

#### 5.5.4 subquery 子查询

子查询可以让多个查询变成一个查询，只要查询一次数据库，性能相对来讲更加高效一点。不用写多条SQL语句就可以实现一些复杂的查询。那么在sqlalchemy中，要实现一个子查询，应该使用下面几个步骤：

1. 将子查询按照传统的方式写好查询语句。然后在query 对象后面执行 subquery 方法。将这个查询编程一个子查询
2. 在子查询中，将以后需要用到的字段通过 label 方法，取个别名。
3. 在福查询中，如果想要使用子查询字段，那么就可以通过子查询的变量上的 c 属性拿到。

整体的实例代码如下：

```python
# encoding: utf-8

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 链接数据库
engine = create_engine('sqlite:///test5.db', echo=True)
# 创建基类
Base = declarative_base(bind=engine)
session = sessionmaker(engine)()


# 实例化数据库
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    age = Column(Integer, default=0)

    def __repr__(self):
        return "<User(username: {}, city: {}, age: {})>".format(
            self.username,
            self.city,
            self.age
        )

# 删除数据库内所有表
# Base.metadata.drop_all()
# 在数据库中创建定义的所有的表
# Base.metadata.create_all()


# 插入数据
# session.add_all([
#     User(username='李A', city='长沙', age=18),
#     User(username='王B', city='长沙', age=18),
#     User(username='赵C', city='北京', age=18),
#     User(username='张D', city='长沙', age=20)

# ])

# 提交数据
# session.commit()

# 寻找和李A这个人在同一个城市，并且是同龄的人
# 第一种方法, 需要两条SQL语句。
# user = session.query(User).filter(User.username == '李A').first()
# users = session.query(User).filter(User.city == user.city, User.age == user.age).all()
# print(users)

# 第二种方式, 能够提升查询性能。
stmt = session.query(User.city.label('city'), User.age.label('age')).filter(User.username=='李A').subquery()

result = session.query(User).filter(User.city == stmt.c.city, User.age == stmt.c.age).all()
print(result)
```

### 5.6 Flask-SQLAlchemy

#### 安装Flask-SQLAlchemy

`pip install flask-sqlalchemy`

#### 数据库连接

1. 定义数据库连接字符串
2. 将这个定义好的数据库连接字符串配置到 app.config 中。实例代码：`app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'`
3. 使用 flask_sqlalchemy.SQLAlchemy 这个类定义一个对象，并将 app 传入进去。示例代码： `db = SQLAlchemy(app)`

#### 创建ORM模型

1. 还是跟使用`sqlalchemy`一样，定义模型，现在不在需要使用 `delarative_base` 来创建基类， 而是使用 db.Model 来作为基类
2. 在模型类中， `Column` 、 `String` 以及 `relationship` 等, 都不需要导入了，直接使用 db 下面的属性名就可以了。
3. 在定义模型的时候，可以不写 `__tablename__` ，那么 flask_sqlalchemy 会默认使用当前模型的名字会转换成小写来作为表的名字，并且如果这个模型的名字使用了多个单词并且使用了驼峰命名法，那么会在多个单词间使用下划线来进行连接，__虽然flask_sqlalchemy给我们提供了这个特性，但是不推荐使用。因为名言胜于暗喻__

#### 将ORM模型映射到数据库

1. db.drop_all()
2. db.create_all()

#### 使用session

以后 `session` 也不需要使用 `sessionmaker` 来创建了，直接使用 `db.session` 就可以了，操作这个 `session` 的时候就跟之前的 `sqlalchemy` 的 `session` 一样。

#### 查询数据

如果查询数据只是查找一个模型上的数据，那么可以通过 `模型.query` 的方式进行查找， `query` 就跟之前的 `sqlalchemy` 中的 `query` 方法是一样的。

### 5.7 alembic 数据库迁移工具

#### 5.7.1 安装

`pip install alembic`

#### 5.7.2 使用alembic步骤

实例文件 > alembic_app 文件夹, alembic仓库是 alembic

1. 定好自己的模型
2. 使用alembic创建一个仓库 alembic init [仓库的名字，推荐使用alembic]
3. 修改配置文件：
    1. 在alembic.ini 中，给sqlalchemy.url 设置数据库的链接方式，这个链接方式跟 sqlalchemy的方式一样。
    2. 在 alembic/env.py 中的 target_metadata 设置模型的 Base.metadata 。但是要导入 models， 需要将models所在的路径添加到这个文件中，实例如下：

    ```python
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from alembic_app.modes import Base
    ```

4. 将ORM模型生成迁移脚本：`alembic revision --autogenerate -m 'first submit'`
5. 将生成的脚本映射到数据库中 `alembic upgrade head`
6. 以后修改了模型，重复 4、5步骤
7. 在终端中，如果想要使用 alembic， 则需要首先进入到安装了 alembic 的虚拟环境中，不然就找不到这个命令。

命令与解释：

1. init： 创建一个alembic仓库
2. revision：创建一个新的版本文件
3. --autogenerate：自动将当前模型的修改，生成迁移脚本
4. -m：本次迁移做了哪些修改，用户可以指定这个参数，方便回顾
5. upgrade：将指定版本的迁移文件映射到数据库中， 会执行脚本文件中的 upgrade 函数。如果有多个迁移脚本没有被映射到数据库中，那么会执行多个迁移脚本
6. [head]：代表最新的迁移脚本的版本号。
7. downgrade：会执行指定版本的迁移文件中的 downgrade 函数。
8. heads：展示 head 指向的脚本文件版本号
9. history：列出所有的迁移版本及其信息
10. current：展示当前数据库中的版本号

另外，在你第一次执行upgrade 的时候，就会在数据库中创建一个名叫 alembic_version 表， 这个表只会有一条数据，记录当前数据库映射的是哪个版本的迁移文件。

##### 5.7.2.1 经典错误

错误描述|原因|解决办法
--|--|--
FAILED：Target database is not up to data.|主要是heads和current不相同。current落后于heads。|将current迁移到head上。alembic upgrade head
FAILED：Can`t locate revision identified by '77525ee61b5b'|数据库中存在的版本号不在迁移脚本文件中|删除数据库的 alembic_version表中的数据，重新执行alembic upgrade head
执行 upgrade head 时报某个表已经存在|执行这个命令的时候会执行所有的迁移脚本，因为数据库中已经存在这个表，迁移脚本中又包含了创建表的代码|1. 删除versions中所有的迁移文件，2. 修改迁移脚本中创建表的代码

#### 5.7.3 flask_script

Flask-Script的作用是可以通过命令行的形式来操作Flask。例如通过命令跑一个开发脚本的服务器、设置数据库，定时任务等。要使用Flask-Script，可以通过 `pip install flask-script` 安装最新版本。

##### 5.7.3.1 命令的添加方式

1. 使用 `manage.commad` 这个方法是用来添加那些不需要传递参数的命令，实例代码如下：

    ```python
    manager = Manager(app)
    manager.add_command('db', db_manager)

    @manager.command
    def greet():
        print('你好')
    ```

2. 使用 `manage.option` 这个方法是用来添加那些需要传递参数的命令。有几个参数就需要写几个 `option`。实例代码如下：

    ```python
    @manager.option('-u', '--username', dest='username')
    @manager.option('-e', '--email', dest='email')
    def add_user(username, email):
        user = BackendUser(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    ```

3. 如果有一些命令是针对某个功能的，比如有一堆命令是针对ORM与表映射的，那么可以将这些命令单独放在一个文件中方便管理。也是使用 `Manager`的对象来添加。然后到注manage文件中，通过 `manager.add_command`来添加。示例代码如下：
db_script.py

    ```python
    form flask_script import Manager

    db_manager = Manager()

    @db_manager.command
    def init():
        print('迁移仓库创建完毕')

    @db_manager.command
    def revision():
        print('迁移脚本生成成功！')

    @db_manager.command
    def upgrade():
        print('脚本映射到数据库成功！')
    ```

#### 5.7.4 flask-migrate

1. 安装 `pip install flask-migrate`

2. 在manage中的代码

    ```python
    from flask_script import Manager
    from run import app
    from ext import db
    from models import User  # 需要把映射到服务器中的模型导入到manage.py文件中
    from flask_migrate import Migrate, MigrateCommand

    manager = Manager(app)
    # 用来绑定APP 和 db到flask_migrage 的
    Migrate(app, db)
    # 添加Migrate的所有命令到db下
    manager.add_command('db', MigrateCommand)


    if __name__ == "__main__":
        manager.run()
    ```

3. flask-migrate常用命令
    1. 初始化一个环境：`python manage.py db init`
    2. 自动检测模型，生成迁移脚本：`python manage.py db migrate`
    3. 将迁移脚本映射到数据库中：`python manage.py db upgrade`
    4. 更多命令：`python manage.py db --help`