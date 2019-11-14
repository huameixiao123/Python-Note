# flask的源码分析

主要来分析`flask`的实例化和在请求来到的收`flask`是如何进行处理的。
## Flask实例化
实例化调用的是`__init__`方法
```python 
    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder="static",
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder="templates",
        instance_path=None,
        instance_relative_config=False,
        root_path=None,
    ):
        # 调用父类的__init__方法 在父类种主要是定义了root_path
        _PackageBoundObject.__init__(
            self, import_name, template_folder=template_folder, root_path=root_path
        )
        # 配置静态文件url 在父类种实现的
        self.static_url_path = static_url_path
        # 配置静态文件目录 在父类中实现的
        self.static_folder = static_folder
        # 配置实例的绝对路径 root_path/instance
        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                "If an instance path is provided it must be absolute."
                " A relative path was given instead."
            )
        # 赋值操作
        self.instance_path = instance_path
        # 默认使用Config类来作为配置文件
        # DENUG 模式设置false
        # 加载默认的配置
        #     default_config = ImmutableDict(
        #     {
        #         "ENV": None,
        #         "DEBUG": None,
        #         "TESTING": False,
        #         "PROPAGATE_EXCEPTIONS": None,
        #         "PRESERVE_CONTEXT_ON_EXCEPTION": None,
        #         "SECRET_KEY": None,
        #         "PERMANENT_SESSION_LIFETIME": timedelta(days=31),
        #         "USE_X_SENDFILE": False,
        #         "SERVER_NAME": None,
        #         "APPLICATION_ROOT": "/",
        #         "SESSION_COOKIE_NAME": "session",
        #         "SESSION_COOKIE_DOMAIN": None,
        #         "SESSION_COOKIE_PATH": None,
        #         "SESSION_COOKIE_HTTPONLY": True,
        #         "SESSION_COOKIE_SECURE": False,
        #         "SESSION_COOKIE_SAMESITE": None,
        #         "SESSION_REFRESH_EACH_REQUEST": True,
        #         "MAX_CONTENT_LENGTH": None,
        #         "SEND_FILE_MAX_AGE_DEFAULT": timedelta(hours=12),
        #         "TRAP_BAD_REQUEST_ERRORS": None,
        #         "TRAP_HTTP_EXCEPTIONS": False,
        #         "EXPLAIN_TEMPLATE_LOADING": False,
        #         "PREFERRED_URL_SCHEME": "http",
        #         "JSON_AS_ASCII": True,
        #         "JSON_SORT_KEYS": True,
        #         "JSONIFY_PRETTYPRINT_REGULAR": False,
        #         "JSONIFY_MIMETYPE": "application/json",
        #         "TEMPLATES_AUTO_RELOAD": None,
        #         "MAX_COOKIE_SIZE": 4093,
        #     }
        # )
        self.config = self.make_config(instance_relative_config)

        # 绑定view_functions 是一个字典
        self.view_functions = {}
        # 绑定error_handler_spec 是一个字典
        self.error_handler_spec = {}
        # url_for异常处理调用的函数列表 
        self.url_build_error_handlers = []
        # 保存before_request 钩子的字典
        self.before_request_funcs = {}
        # 保存before_first_request钩子函数的列表
        self.before_first_request_funcs = []
        # 保存after_request 钩子函数的字典
        self.after_request_funcs = {}
        # 保存teardown_request钩子函数
        self.teardown_request_funcs = {}
        # 保存teardown_appcontext 钩子函数
        self.teardown_appcontext_funcs = []
        # 保存 url_value_preprocessor 钩子函数
        self.url_value_preprocessors = {}

        # url 默认处理函数
        self.url_default_functions = {}
        # 上下文处理器context_processor 装饰器钩子函数
        # 默认添加了 request session g 这三个对象
        self.template_context_processors = {None: [_default_template_ctx_processor]}

        # 当使用shell时候被调用
        self.shell_context_processors = []

        # 绑定的蓝图 保存蓝图
        self.blueprints = {}
        # 绑定_blueprint_order 属性 作为蓝图排序用的
        self._blueprint_order = []

        # app 扩展的属性
        self.extensions = {}

        #: The :class:`~werkzeug.routing.Map` for this instance.  You can use
        #: this to change the routing converters after the class was created
        #: but before any routes are connected.  Example::
        #:
        #:    from werkzeug.routing import BaseConverter
        #:
        #:    class ListConverter(BaseConverter):
        #:        def to_python(self, value):
        #:            return value.split(',')
        #:        def to_url(self, values):
        #:            return ','.join(super(ListConverter, self).to_url(value)
        #:                            for value in values)
        #:
        #:    app = Flask(__name__)
        #:    app.url_map.converters['list'] = ListConverter
        # url 转换器配置类
        # from werkzeug.routing import Map
        #  self.url_map_class == Map()
        self.url_map = self.url_map_class()
        # host_matching 默认是False
        self.url_map.host_matching = host_matching
        # 属性绑定subdomain_matching 默认是False
        self.subdomain_matching = subdomain_matching

        # tracks internally if the application already handled at least one
        # request.
        # 属性绑定  是否处理了第一个请求
        self._got_first_request = False
        # 属性绑定   Lock() 锁
        # from threading import Lock
        self._before_request_lock = Lock()
        # 添加静态文件的路由
        if self.has_static_folder:
            # 判断是否添加了host 
            assert (
                bool(static_host) == host_matching
            ), "Invalid static_host/host_matching combination"
            self.add_url_rule(
                self.static_url_path + "/<path:filename>",
                # /static/<path:filename>
                endpoint="static",
                host=static_host,
                # 调用的试图函数 
                view_func=self.send_static_file,
            )

        # 针对cli命令行程序的
        self.cli.name = self.name
```
整理下flask在初始化的时候做的事情 
1. 添加了默认的配置类和debug模式
2. 配置了静态文件路径和模板文件路径以及如何访问
3. 定义了很多个钩子函数 
4. 定义了url匹配的类
5. 定义了蓝图相关的配置
6. 默认定义的上下文处理器 
7. 定义了视图函数的容器
8. 错误处理的装饰器


## flask处理请求

在调试的时候是调用的`flask`提供的测试服务器，在生产环境中，是使用`uwsgi`或者`gunicorn`来启动`flask`应用的。这里分析的是在生产环境的代码走向。

`flask`应用请求到来的时候会调用`app.__call__()`方法，看下这个方法的代码：

```python
def __call__(self, environ, start_response):
    return self.wsgi_app(environ, start_response)
```
可以看到这个代码的返回值是调用了`app.wsgi_app(environ, start_response)`方法。
继续看`app.wsgi_app(environ, start_response)`的代码,由于代码比较长就写在注释里面。
```python 
    def wsgi_app(self, environ, start_response):
        # 通过environ来生成一个上下文对象，
        ctx = self.request_context(environ)
        # 定义错误处理
        error = None
        # 进行业务处理
        try:
            try:
                # 将请求上下文推入栈中
                ctx.push()
                # 处理请求得到响应对象response
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                # 将错误处理转换成response对象
                response = self.handle_exception(e)
            # 非Exception异常处理
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            # 将响应结果返回
            return response(environ, start_response)
        finally:
            # 判断是否要忽略错误，默认是False，如果是True，将error=None
            if self.should_ignore_error(error):
                error = None
            # 清除上下文数据
            ctx.auto_pop(error)
```
分析 `self.request_context(environ)`

```python
def request_context(self, environ):
    return RequestContext(self, environ)

#  RequestContext的init方法
def __init__(self, app, environ, request=None, session=None):
    self.app = app
    # 如果request是None的话，也就是flask服务启动的时候
    # 将environ包装成Request(environ)对象这个对象是flask对werkzeug里面的request封装
    if request is None:
        request = app.request_class(environ)
    # 将封装好的Request对象绑定在请求上下文上
    self.request = request
    # 在请求上下文中绑定url_adapter属性，默认是None
    # url_adapter url适配器
    self.url_adapter = None
    try:
        self.url_adapter = app.create_url_adapter(self.request)
    except HTTPException as e:
        self.request.routing_exception = e
    self.flashes = None
    self.session = session
    self._implicit_app_ctx_stack = []
    self.preserved = False
    self._preserved_exc = None
    self._after_request_functions = []

```
create_url_adapter函数：
```python
    def create_url_adapter(self, request):
        if request is not None:
            subdomain = (
                (self.url_map.default_subdomain or None)
                if not self.subdomain_matching
                else None
            )
            return self.url_map.bind_to_environ(
                request.environ,
                server_name=self.config["SERVER_NAME"],
                subdomain=subdomain,
            )
        if self.config["SERVER_NAME"] is not None:
            return self.url_map.bind(
                self.config["SERVER_NAME"],
                script_name=self.config["APPLICATION_ROOT"],
                url_scheme=self.config["PREFERRED_URL_SCHEME"],
            )

```


