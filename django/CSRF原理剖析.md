## 什么是CSRF
CSRF（Cross Site Request Forgery, 跨站域请求伪造）是一种网络的攻击方式，它在 2007 年曾被列为互联网 20 大安全隐患之一。其他安全隐患，比如 SQL 脚本注入，跨站域脚本攻击等在近年来已经逐渐为众人熟知，很多网站也都针对他们进行了防御。然而，对于大多数人来说，CSRF 却依然是一个陌生的概念。即便是大名鼎鼎的 Gmail, 在 2007 年底也存在着 CSRF 漏洞，从而被黑客攻击而使 Gmail 的用户造成巨大的损失。
## CSRF原理
网站是通过cookie来实现登录功能的。而cookie只要存在浏览器中，那么浏览器在访问这个cookie的服务器的时候，就会自动的携带cookie信息到服务器上去。那么这时候就存在一个漏洞了，如果你访问了一个别有用心或病毒网站，这个网站可以在网页源代码中插入js代码，使用js代码给其他服务器发送请求（比如ICBC的转账请求）。那么因为在发送请求的时候，浏览器会自动的把cookie发送给对应的服务器，这时候相应的服务器（比如ICBC网站），就不知道这个请求是伪造的，就被欺骗过去了。从而达到在用户不知情的情况下，给某个服务器发送了一个请求（比如转账）。

## 解决方案
CSRF攻击的要点就是在向服务器发送请求的时候，相应的cookie会自动的发送给对应的服务器。造成服务器不知道这个请求是用户发起的还是伪造的。这时候，我们可以在用户每次访问有表单的页面的时候，在网页源代码中加一个随机的字符串叫做csrf_token，在cookie中也加入一个相同值的csrf_token字符串。以后给服务器发送请求的时候，必须在body中以及cookie中都携带csrf_token，服务器只有检测到cookie中的csrf_token和body中的csrf_token都相同，才认为这个请求是正常的，否则就是伪造的。那么黑客就没办法伪造请求了

## django中CSRF是如何解决的
在Django中，如果想要防御CSRF攻击，应该做两步工作。第一个是在settings.MIDDLEWARE中添加CsrfMiddleware中间件。第二个是在模版代码中添加一个input标签，加载csrf_token。示例代码如下：
服务器代码：
```python
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.gzip.GZipMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware', # CSRF中间件
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
```
在模版中使用
```html
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}"/>
```
或者是直接使用csrf_token标签，来自动生成一个带有csrf token的input标签：
`{% csrf_token %}`

## 使用ajax处理csrf防御：
如果用ajax来处理csrf防御，那么需要手动的在form中添加csrfmiddlewaretoken，或者是在请求头中添加X-CSRFToken。我们可以从返回的cookie中提取csrf token，再设置进去。示例代码如下：
```js
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var myajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
};

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var money = $("input[name='money']").val();

        myajax.post({
            'url': '/transfer/',
            'data':{
                'email': email,
                'money': money
            },
            'success': function (data) {
                console.log(data);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    })
});
```


## Django中CSRF中间件的代码剖析
csrf中间件`django.middleware.csrf.CsrfViewMiddleware`有3个钩子函数
process_request
process_view
process_response

代码
```python 
    def process_request(self, request):
        csrf_token = self._get_token(request)
        if csrf_token is not None:
            request.META['CSRF_COOKIE'] = csrf_token
     def process_view(self, request, callback, callback_args, callback_kwargs):
        if getattr(request, 'csrf_processing_done', False):
            return None

        if getattr(callback, 'csrf_exempt', False):
            return None

        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if getattr(request, '_dont_enforce_csrf_checks', False):
                return self._accept(request)

            if request.is_secure():
                referer = request.META.get('HTTP_REFERER')
                if referer is None:
                    return self._reject(request, REASON_NO_REFERER)

                referer = urlparse(referer)

                if '' in (referer.scheme, referer.netloc):
                    return self._reject(request, REASON_MALFORMED_REFERER)

                if referer.scheme != 'https':
                    return self._reject(request, REASON_INSECURE_REFERER)
                good_referer = (
                    settings.SESSION_COOKIE_DOMAIN
                    if settings.CSRF_USE_SESSIONS
                    else settings.CSRF_COOKIE_DOMAIN
                )
                if good_referer is not None:
                    server_port = request.get_port()
                    if server_port not in ('443', '80'):
                        good_referer = '%s:%s' % (good_referer, server_port)
                else:
                    # request.get_host() includes the port.
                    good_referer = request.get_host()

                good_hosts = list(settings.CSRF_TRUSTED_ORIGINS)
                good_hosts.append(good_referer)

                if not any(is_same_domain(referer.netloc, host) for host in good_hosts):
                    reason = REASON_BAD_REFERER % referer.geturl()
                    return self._reject(request, reason)

            csrf_token = request.META.get('CSRF_COOKIE')
            if csrf_token is None:
                
                return self._reject(request, REASON_NO_CSRF_COOKIE)

            request_csrf_token = ""
            if request.method == "POST":
                try:
                    request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
                except IOError:
                    pass

            if request_csrf_token == "":
                request_csrf_token = request.META.get(settings.CSRF_HEADER_NAME, '')

            request_csrf_token = _sanitize_token(request_csrf_token)
            if not _compare_salted_tokens(request_csrf_token, csrf_token):
                return self._reject(request, REASON_BAD_TOKEN)

        return self._accept(request)

    def process_response(self, request, response):
        if not getattr(request, 'csrf_cookie_needs_reset', False):
            if getattr(response, 'csrf_cookie_set', False):
                return response

        if not request.META.get("CSRF_COOKIE_USED", False):
            return response
        self._set_token(request, response)
        response.csrf_cookie_set = True
        return response
```

1. 请求进来首先执行process_request方法
```python
def process_request(self, request):
        csrf_token = self._get_token(request) # 获取cookie里面的token
        if csrf_token is not None:
            request.META['CSRF_COOKIE'] = csrf_token
            # 给request对象添加一个META属性CSRF_COOKIE= cookie里面的token
# 这一步主要是在request.META绑定一个CSRF_COOKIE的属性 
```
调用`self._get_token(request)`方法
```python 
    def _get_token(self, request):
        if settings.CSRF_USE_SESSIONS: #  默认 CSRF_USE_SESSIONS = False
            try:
                return request.session.get(CSRF_SESSION_KEY)
            except AttributeError:
                raise ImproperlyConfigured(
                    'CSRF_USE_SESSIONS is enabled, but request.session is not '
                    'set. SessionMiddleware must appear before CsrfViewMiddleware '
                    'in MIDDLEWARE%s.' % ('_CLASSES' if settings.MIDDLEWARE is None else '')
                )
        else:
            try:
                cookie_token = request.COOKIES[settings.CSRF_COOKIE_NAME] # CSRF_COOKIE_NAME = 'csrftoken' 判断cookie里是否有csrf这个键
            except KeyError:
                return None

            csrf_token = _sanitize_token(cookie_token)
            # 对csrf进行清洗，返回一个64位的包含数字和字母的字符串
            if csrf_token != cookie_token:
                # 判断清洗后的token和cookie里面的token是否一致，如果不一致就会给request对象绑定一个csrf_cookie_needs_reset=True的属性
                request.csrf_cookie_needs_reset = True
            # 最后返回清洗后的token
            return csrf_token

    def _sanitize_token(token):
        # CSRF_SECRET_LENGTH = 32
        # CSRF_TOKEN_LENGTH = 2 * CSRF_SECRET_LENGTH
        # CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits
        # CSRF_SESSION_KEY = '_csrftoken'
        # 判断获取到的csrf值是否是由字母和数字组成，不是的话获取一个新的csrf值
        if re.search('[^a-zA-Z0-9]', token):
            return _get_new_csrf_token()
        # 判断token的长度是否是64位 是的话值金额返回token
        elif len(token) == CSRF_TOKEN_LENGTH:
            return token
        # 判断token的长度是不是等于32位，是的话对token加盐处理成64位返回
        elif len(token) == CSRF_SECRET_LENGTH:
            return _salt_cipher_secret(token)
        # 如果都不满足的话重新生成一个token
        return _get_new_csrf_token()
    def _salt_cipher_secret(secret):
        salt = _get_new_csrf_string() # 获取一个32位随机的字符串
        chars = CSRF_ALLOWED_CHARS
        pairs = zip((chars.index(x) for x in secret), (chars.index(x) for x in salt))
        # pairs = zip((23,24)...)
        cipher = ''.join(chars[(x + y) % len(chars)] for x, y in pairs)
        # 生成32位的字符串加上salt返回
        return salt + cipher

```
2. 下来执行`process_view()`方法
```python 
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 获取request上面的csrf_processing_done属性，这个属性是标志csrf是否完成校验，如果完成则返回None继续执行其他中间件
        if getattr(request, 'csrf_processing_done', False):
            return None
        # 判断视图函数中是否启用了csrf忽略的装饰器，启动了的话就会返回None继续执行剩下的中间件
        if getattr(callback, 'csrf_exempt', False):
            return None

       
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            # 在测试环境中不使用csrf校验，所以会忽略csrf的校验
            if getattr(request, '_dont_enforce_csrf_checks', False):
                return self._accept(request)
            # 如果是HTTPS的请求
            if request.is_secure():
                # 获取请求的前拽
                referer = request.META.get('HTTP_REFERER')
                # 如果没有则拒绝通过校验
                if referer is None:
                    return self._reject(request, REASON_NO_REFERER)
                # 解析https请求的HTTP_REFERER
                referer = urlparse(referer)

                # 如果无法解析出域名信息就拒绝
                if '' in (referer.scheme, referer.netloc):
                    return self._reject(request, REASON_MALFORMED_REFERER)

                # 不是https请求拒绝
                if referer.scheme != 'https':
                    return self._reject(request, REASON_INSECURE_REFERER)

                good_referer = (
                    settings.SESSION_COOKIE_DOMAIN
                    if settings.CSRF_USE_SESSIONS
                    else settings.CSRF_COOKIE_DOMAIN
                )
                if good_referer is not None:
                    server_port = request.get_port()
                    if server_port not in ('443', '80'):
                        good_referer = '%s:%s' % (good_referer, server_port)
                else:
                    # 获取主机和端口
                    good_referer = request.get_host()

                # Here we generate a list of all acceptable HTTP referers,
                # including the current host since that has been validated
                # upstream.
                good_hosts = list(settings.CSRF_TRUSTED_ORIGINS)
                good_hosts.append(good_referer)
                # 不是本域名的请求拒绝
                if not any(is_same_domain(referer.netloc, host) for host in good_hosts):
                    reason = REASON_BAD_REFERER % referer.geturl()
                    return self._reject(request, reason)
            # 从request.META获取token
            csrf_token = request.META.get('CSRF_COOKIE')
            if csrf_token is None:
                # 如果没有tokon就拒绝
                return self._reject(request, REASON_NO_CSRF_COOKIE)

            # Check non-cookie token for match.
            # 检查不是通过cookie匹配的token
            request_csrf_token = ""
            # 如果是post请求 首先获取csrfmiddlewaretoken的值
            if request.method == "POST":
                try:
                    request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
                except IOError:
                    # Handle a broken connection before we've completed reading
                    # the POST data. process_view shouldn't raise any
                    # exceptions, so we'll ignore and serve the user a 403
                    # (assuming they're still listening, which they probably
                    # aren't because of the error).
                    pass
            # 没有获取到的话是 request.META 中获取头信息HTTP_X_CSRFTOKEN
            # CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
            if request_csrf_token == "":
                # Fall back to X-CSRFToken, to make things easier for AJAX,
                # and possible for PUT/DELETE.
                request_csrf_token = request.META.get(settings.CSRF_HEADER_NAME, '')
            # 如果还没有就重新生成一个token
            request_csrf_token = _sanitize_token(request_csrf_token)
            # 判断请求的csrftoken和request.META中是否一致 不一致就拒绝
            if not _compare_salted_tokens(request_csrf_token, csrf_token):
                return self._reject(request, REASON_BAD_TOKEN)
         # 如果请求方式是'GET', 'HEAD', 'OPTIONS', 'TRACE'则不必要执行csrf校验
         # 将request.csrf_processing_done设置成True
        return self._accept(request)
```
```python 
    def _accept(self, request):
        request.csrf_processing_done = True
        return None
```
3. process_response
```python 
   def process_response(self, request, response):
        # 在cookie中设置csrftoken
        # 如果csrf_cookie_needs_reset=False 并且response中csrf_cookie_set=True
        # 直接返回response不需要设置csrftoken
        if not getattr(request, 'csrf_cookie_needs_reset', False):
            if getattr(response, 'csrf_cookie_set', False):
                return response
        # 如果请求里面的CSRF_COOKIE_USED=False的话，证明csrf没有被校验过，可以继续使用，不需要重新设置
        if not request.META.get("CSRF_COOKIE_USED", False):
            return response

        # Set the CSRF cookie even if it's already set, so we renew
        # the expiry timer.、
        # 设置csrftoken
        self._set_token(request, response)
        # 给response添加一个csrf_cookie_set=True的属性，说明csrf已经设置过了
        response.csrf_cookie_set = True
        return response
```

## 总结
使用csrf保护，首先要开启csrf中间件，然后在模版中，或者在视图中启用csrf也就是本质上调用`get_token()`这个函数，在模版中可以使用`｛% csrf_token %｝` 或者使用input标签`<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">`,如果使用的是ajax发送请求的话，可以在meta标签中加载csrf_token的值，也可以在视图函数中添加装饰器`from django.views.decorators.csrf import ensure_csrf_cookie`.