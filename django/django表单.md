# 表单

## HTML中的表单

单纯从前端的 `html`来说，表单是用来提交数据给服务器的,不管后台的服务器用的是 `Django`还是 `PHP`语言还是其他语言。只要把 `input`标签放在 `form`标签中，然后再添加一个提交按钮，那么以后点击提交按钮，就可以将 `input`标签中对应的值提交给服务器了。

## Django中的表单

`Django`中的表单丰富了传统的 `HTML`语言中的表单。在 `Django`中的表单，主要做以下两件事：
1. 渲染表单模板。
2. 表单验证数据是否合法。

## Django中表单使用流程

1. 编写表单类
在讲解 `Django`表单的具体每部分的细节之前。我们首先先来看下整体的使用流程。这里以一个做一个留言板为例。首先我们在后台服务器定义一个表单类，继承自 django.forms.Form 。示例代码如下：
```python
    # forms.py
    class MessageBoardForm(forms.Form):
        title = forms.CharField(max_length=3,label='标题',min_length=2,error_messages={"min_length":'标题字符段不符合要求！'})
        content = forms.CharField(widget=forms.Textarea,label='内容')
        email = forms.EmailField(label='邮箱')
        reply = forms.BooleanField(required=False,label='回复')
```
每个Django表单的实例都有一个内置的`is_valid()`方法，用来验证接收的数据是否合法。如果所有数据都合法，那么该方法将返回True，并将所有的表单数据转存到它的一个叫做`cleaned_data`的属性中，该属性是以个字典类型数据。

2. 视图处理
然后在视图中，根据是 `GET`还是 `POST`请求来做相应的操作。如果是 `GET`请求，那么返回一个空的表单，如果是 `POST`请求，那么将提交上来的数据进行校验。示例代码如下：
```python
    # views.py
    class IndexView(View):
        def get(self,request):
            form = MessageBoardForm()
            return render(request,'index.html',{'form':form})
            
        def post(self,request):
            form = MessageBoardForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                email = form.cleaned_data.get('email')
                reply = form.cleaned_data.get('reply')
                return HttpResponse('success')
            else:
                print(form.errors)
                return HttpResponse('fail')
```
3. 模板处理
在使用 `GET`请求的时候，我们传了一个 `form`给模板，那么以后模板就可以使用 `form`来生成一个表单的 `html`代码。在使用 `POST`请求的时候，我们根据前端上传上来的数据，构建一个新的表单，这个表单是用来验证数据是否合法的，如果数据都验证通过了，那么我们可以通过 `cleaned_data`来获取相应的数据。在模板中渲染表单的 HTML 代码如下：
```html
    <form action="" method="post">
        <table>
            {{ form.as_table }}
            <tr>
                <td></td>
                <td><input type="submit" value="提交"></td>
            </tr>
        </table>
    </form>
```
要点：

    + `<form>...</form>`标签要自己写；
    + 使用POST的方法时，必须添加`{% csrf_token %}`标签，用于处理csrf安全机制；
{{ form }}代表Django为你生成其它所有的form标签元素，也就是我们上面做的事情；
提交按钮需要手动添加！
提示：默认情况下，Django支持HTML5的表单验证功能，比如邮箱地址验证、必填项目验证等等
一定要**注意**，它不包含`<form>`标签本身以及提交按钮！！！为什么要这样？方便你自己控制表单动作和CSS，JS以及其它类似bootstrap框架的嵌入！
我们在最外面给了一个 `form`标签，然后在里面使用了 `table`标签来进行美化，在使用 `form`对象渲染的时候，使用的是 `table`的方式，当然还可以使用 `ul`的方式（ `as_ul` ），也可以使用 `p`标签的方式（ `as_p`），并且在后面我们还加上了一个提交按钮。这样就可以生成一个表单了

### 高级技巧

每一个表单字段类型都对应一种`Widget`类，每一种`Widget`类都对应了HMTL语言中的一种`input`元素类型，比如`<input type="text">`。需要在HTML中实际使用什么类型的input，就需要在Django的表单字段中选择相应的field。比如要一个`<input type="text">`，可以选择一个`CharField`。

一旦你的表单接收数据并验证通过了，那么就可以从form.cleaned_data字典中读取所有的表单数据，下面是一个例子：
```python
# views.py

from django.core.mail import send_mail

if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)

    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/')
```

### 使用表单模板

1 . 表单渲染格式
前面我们通过`{{ form }}`模板语言，简单地将表单渲染到HTML页面中了，实际上，有更多的方式：
    + `{{ form.as_table }}`将表单渲染成一个表格元素，每个输入框作为一个`<tr>`标签
    + `{{ form.as_p }}` 将表单的每个输入框包裹在一个`<p>`标签内 tags
    + `{{ form.as_ul }}` 将表单渲染成一个列表元素，每个输入框作为一个`<li>`标签

注意：你要自己手动编写`<table>`和`<ul>`标签。

下面是将上面的`ContactForm`作为`{{ form.as_p }}`的例子：
```html
<p><label for="id_subject">Subject:</label>
    <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>
<p><label for="id_message">Message:</label>
    <textarea name="message" id="id_message" required></textarea></p>
<p><label for="id_sender">Sender:</label>
    <input type="email" name="sender" id="id_sender" required /></p>
<p><label for="id_cc_myself">Cc myself:</label>
    <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
```
注意：Django自动为每个input元素设置了一个id名称，对应label的for参数。

2 . 手动渲染表单字段
直接`{{ form }}`虽然好，啥都不用操心，但是往往并不是你想要的，比如你要使用CSS和JS，比如你要引入Bootstarps框架，这些都需要对表单内的input元素进行额外控制，那怎么办呢？手动渲染字段就可以了。

可以通过`{{ form.name_of_field }}`获取每一个字段，然后分别渲染，如下例所示：
```html
{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>
```
其中的`label`标签甚至可以用`label_tag()`方法来生成，于是可以简写成下面的样子:
```html
<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>
```
这样子是不是更加灵活了呢？但是灵活的代价就是我们要写更多的代码，又偏向原生的HTML代码多了一点。

3 . 渲染表单错误信息：
注意上面的例子中，我们使用`{{ form.name_of_field.errors }}`模板语法，在表单里处理错误信息。对于每一个表单字段的错误，它其实会实际生成一个无序列表，参考下面的样子：
```html
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>
```
这个列表有个默认的CSS样式类`errorlist`，如果你想进一步定制这个样式，可以循环错误列表里的内容，然后单独设置样式：
```html
{% if form.subject.errors %}
    <ol>
    {% for error in form.subject.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif %}
```
一切非字段的错误信息，比如表单的错误，隐藏字段的错误都保存在`{{ form.non_field_errors }}`中，上面的例子，我们把它放在了表单的外围上面，它将被按下面的HTML和CSS格式渲染：
```html
<ul class="errorlist nonfield">
    <li>Generic validation error</li>
</ul>
```

4 . 循环表单的字段
如果你的表单字段有相同格式的HMTL表现，那么完全可以循环生成，不必要手动的编写每个字段，减少冗余和重复代码，只需要使用模板语言中的`{% for %}`循环，如下所示：
```html
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}
```
下表是`{{ field }}`中非常有用的属性，这些都是Django内置的模板语言给我们提供的方便：

|属性|	说明|
|--- |---|
|`{{ field.label }}`|	字段对应的label信息|
|`{{ field.label_tag }}`|	自动生成字段的label标签，注意与`{{ field.label }}`的区别。|
|`{{ field.id_for_label }}`|	自定义字段标签的id|
|`{{ field.value }}`|	当前字段的值，比如一个`Email`字段的值`someone@example.com`|
|`{{ field.html_name }}`|	指定字段生成的`inpu`t标签中`name`属性的值|
|`{{ field.help_text }}`|	字段的帮助信息|
|`{{ field.errors }}`|	包含错误信息的元素|
|`{{ field.is_hidden }}`|	用于判断当前字段是否为隐藏的字段，如果是，返回True|
|`{{ field.field }}`|	返回字段的参数列表。例如`{{ char_field.field.max_length }}`|

5 . 不可见字段的特殊处理
很多时候，我们的表单中会有一些隐藏的不可见的字段，比如honeypot。我们需要让它在任何时候都仿佛不存在一般，比如有错误的时候，如果你在页面上显示了不可见字段的错误信息，那么用户会很迷惑，这是哪来的呢？所以，通常我们是不显示不可见字段的错误信息的。

Django提供了两种独立的方法，用于循环那些不可见的和可见的字段，`hidden_fields()`和`visible_fields()`。这里，我们可以稍微修改一下前面的例子：
```html
{# 循环那些不可见的字段 #}
{% for hidden in form.hidden_fields %}
{{ hidden }}
{% endfor %}
{# 循环可见的字段 #}
{% for field in form.visible_fields %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```

6 . 重用表单模板
如果你在自己的HTML文件中，多次使用同一种表单模板，那么你完全可以把表单模板存成一个独立的HTML文件，然后在别的HTML文件中通过include模板语法将其包含进来，如下例所示：
```html
# 实际的页面文件中:
{% include "form_snippet.html" %}

-----------------------------------------------------

# 单独的表单模板文件form_snippet.html:
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
如果你的页面同时引用了好几个不同的表单模板，那么为了防止冲突，你可以使用with参数，给每个表单模板取个别名，如下所示：
```html
{% include "form_snippet.html" with form=comment_form %}
```
在使用的时候就是：
```html
{% for field in comment_form %}
......
```
如果你经常做这些重用的工作，建议你考虑自定义一个内联标签，这已经是Django最高级的用法了。

# 用表单验证数据

## 常用的Field

使用 `Field`可以是对数据验证的第一步。你期望这个提交上来的数据是什么类型，那么就使用什么类型的 Field 。

### CharField

用来接收文本。
参数：
+ max_length：这个字段值的最大长度。
+ min_length：这个字段值的最小长度。
+ required：这个字段是否是必须的。默认是必须的。
+ error_messages：在某个条件验证失败的时候，给出错误信息。

### EmailField

用来接收邮件，会自动验证邮件是否合法。
错误信息的key： required 、 invalid。

### FloatField

用来接收浮点类型，并且如果验证通过后，会将这个字段的值转换为浮点类型。参数：
+ max_value：最大的值。
+ min_value：最小的值。
错误信息的key： `required`、 `invalid`、 `max_value`、 `min_value`。

### IntegerField

用来接收整形，并且验证通过后，会将这个字段的值转换为整形。参数：
+ max_value：最大的值。
+ min_value：最小的值。
错误信息的key： `required`、 `invalid`、 `max_value`、 `min_value`。

### URLField

用来接收 url 格式的字符串。
错误信息的key： `required`、 `invalid `。


## 常用验证器

在验证某个字段的时候，可以传递一个 `validators`参数用来指定验证器，进一步对数据进行过滤。验证器有很多，但是很多验证器我们其实已经通过这个 Field 或者一些参数就可以指定了。比如 `EmailValidator`，我们可以通过 `EmailField`来指定，比如 `MaxValueValidator`，我们可以通过 `max_value`参数来指定。以下是一些常用的验证器：
1. `MaxValueValidator`：验证最大值。
2. `MinValueValidator`：验证最小值。
3. `MinLengthValidator`：验证最小长度。
4. `MaxLengthValidator`：验证最大长度。
5. `EmailValidator`：验证是否是邮箱格式。
6. `URLValidator`：验证是否是 URL 格式。
7. `RegexValidator`：如果还需要更加复杂的验证，那么我们可以通过正则表达式的验证器： RegexValidator 。比如现在要验证手机号码是否合格，那么我们可以通过以下代码实现：
```python
    class MyForm(forms.Form):
        telephone = forms.CharField(validators=[validators.RegexValidator("1[345678]\d{9}",message='请输入正确格式的手机号码！')])
```

## 自定义验证

有时候对一个字段验证，不是一个长度，一个正则表达式能够写清楚的，还需要一些其他复杂的逻辑，那么我们可以对某个字段，进行自定义的验证。比如在注册的表单验证中，我们想要验证手机号码是否已经被注册过了，那么这时候就需要在数据库中进行判断才知道。对某个字段进行自定义的验证方式是，定义一个方法，这个方法的名字定义规则是： `clean_fieldname`。如果验证失败，那么就抛出一个验证错误。比如要验证用户表中手机号码之前是否在数据库中存在，那么可以通过以下代码实现：
```python
    class MyForm(forms.Form):
    telephone = forms.CharField(validators=[validators.RegexValidator("1[345678]\d{9}",message='请输入正确格式的手机号码！')])
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("手机号码已经存在！")
        return telephone
```
以上是对某个字段进行验证，如果验证数据的时候，需要针对多个字段进行验证，那么可以重写 `clean`方法。比如要在注册的时候，要判断提交的两个密码是否相等。那么可以使用以下代码来完成：
```python
    class MyForm(forms.Form):
        telephone = forms.CharField(validators=[validators.RegexValidator("1[345678]\d{9}",message='请输入正确格式的手机号码！')])
        pwd1 = forms.CharField(max_length=12)
        pwd2 = forms.CharField(max_length=12)
    
        def clean(self):
            cleaned_data = super().clean()
            pwd1 = cleaned_data.get('pwd1')
            pwd2 = cleaned_data.get('pwd2')
            if pwd1 != pwd2:
            raise forms.ValidationError('两个密码不一致！')
```

## 提取错误信息

如果验证失败了，那么有一些错误信息是我们需要传给前端的。这时候我们可以通过以下属性来获取：
1. `form.errors` ：这个属性获取的错误信息是一个包含了 `html`标签的错误信息。
2. `form.errors.get_json_data()` ：这个方法获取到的是一个字典类型的错误信息。将某个字段的名字作为 key ，错误信息作为值的一个字典。
3. `form.as_json()` ：这个方法是将 `form.get_json_data()` 返回的字典 dump 成 json 格式的字符串，方便进行传输。
4. 上述方法获取的字段的错误值，都是一个比较复杂的数据。比如以下：
```python
    {'username': [{'message': 'Enter a valid URL.', 'code': 'invalid'}, {'message': 'Ensure this value has at most 4 characters (it has 22).', 'code': 'max_length'}]}
```
那么如果我只想把错误信息放在一个列表中，而不要再放在一个字典中。这时候我们可以定义一个方法，把这个数据重新整理一份。实例代码如下：
```python
    class MyForm(forms.Form):
        username = forms.URLField(max_length=4)
        
        def get_errors(self):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key,message_dicts in errors.items():
                messages = []
                    for message in message_dicts:
                        messages.append(message['message'])
                    new_errors[key] = messages
            return new_errors
```
这样就可以把某个字段所有的错误信息直接放在这个列表中。

# ModelForm

大家在写表单的时候，会发现表单中的 `Field`和模型中的 `Field`基本上是一模一样的，而且表单中需要验证的数据，也就是我们模型中需要保存的。那么这时候我们就可以将模型中的字段和表单中的字段进行绑定。
比如现在有个 Article 的模型。示例代码如下：
```python
    from django.db import models
    from django.core import validators
    
    class Article(models.Model):
        title = models.CharField(max_length=10,validators=[validators.MinLengthValidator(limit_value=3)])
        content = models.TextField()
        author = models.CharField(max_length=100)
        category = models.CharField(max_length=100)
        create_time = models.DateTimeField(auto_now_add=True)
```
那么在写表单的时候，就不需要把 `Article`模型中所有的字段都一个个重复写一遍了。示例代码如下：
```python
    from django import forms
    
    class MyForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = "__all__"
```
`MyForm`是继承自 `forms.ModelForm` ，然后在表单中定义了一个 `Meta`类，在 `Meta`类中指定了 `model=Article` ，以及 `fields="__all__"` ，这样就可以将 `Article `模型中所有的字段都复制过来，进行验证。如果只想针对其中几个字段进行验证，那么可以给 `fields`指定一个列表，将需要的字段写进去。比如只想验证 `title`和 `content`，那么可以使用以下代码实现：
```python
    from django import forms
    
    class MyForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title','content']
```
如果要验证的字段比较多，只是除了少数几个字段不需要验证，那么可以使用 `exclude`来代替 `fields`。比如我不想验证 `category`，那么示例代码如下：
```python
    class MyForm(forms.ModelForm):
        class Meta:
            model = Article
            exclude = ['category']
```

## 自定义错误消息

使用 `ModelForm`，因为字段都不是在表单中定义的，而是在模型中定义的，因此一些错误消息无法在字段中定义。那么这时候可以在 `Meta`类中，定义 `error_messages`，然后把相应的错误消息写到里面去。示例代码如下：
```python
    class MyForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['category']
        error_messages ={
            'title':{
                'max_length': '最多不能超过10个字符！',
                'min_length': '最少不能少于3个字符！'
            },
            'content': {
                'required': '必须输入content！',
            }
        }
```

### save方法

`ModelForm`还有 `save`方法，可以在验证完成后直接调用 `save`方法，就可以将这个数据保存到数据库中了。示例代码如下：
```python
    form = MyForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse('succes')
    else:
        print(form.get_errors())
        return HttpResponse('fail')
```
这个方法必须要在 `clean`没有问题后才能使用，如果在 `clean`之前使用，会抛出异常。另外，我们在调用 `save`方法的时候，如果传入一个 `commit=False` ，那么只会生成这个模型的对象，而不会把这个对象真正的插入到数据库中。比如表单上验证的字段没有包含模型中所有的字段，这时候就可以先创建对象，再根据填充其他字段，把所有字段的值都补充完成后，再保存到数据库中。示例代码如下：
```python
    form = MyForm(request.POST)
    if form.is_valid():
        article = form.save(commit=False)
        article.category = 'Python'
        article.save()
        return HttpResponse('succes')
    else:
        print(form.get_errors())
        return HttpResponse('fail')
```

### ModelForm的验证

验证ModelForm主要分两步：
    + 验证表单
    + 验证模型实例
    
与普通的表单验证类似，模型表单的验证也是调用`is_valid()`方法或访问`errors`属性。模型的验证（`Model.full_clean()`）紧跟在表单的`clean()`方法调用之后。通常情况下，我们使用Django内置的验证器就好了。如果需要，可以重写模型表单的`clean()`来提供额外的验证，方法和普通的表单一样。

### ModelForm的字段选择

强烈建议使用`ModelForm`的`fields`属性，在赋值的列表内，一个一个将要使用的字段添加进去。这样做的好处是，安全可靠。
然而，有时候，字段太多，或者我们想偷懒，不愿意一个一个输入，也有简单的方法：
`__all__`:
将fields属性的值设为`__all__`，表示将映射的模型中的全部字段都添加到表单类中来。
```python
from django.forms import ModelForm

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
```

**exclude**属性

表示将model中，除了exclude属性中列出的字段之外的所有字段，添加到表单类中作为表单字段。
```python
class PartialAuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = ['birth_date']
```
因为`Author`模型有3个字段`name`、`title`和`birth_date`，上面的例子会让`title`和`name`出现在表单中。

### 自定义ModelForm字段

在前面，我们有个表格，展示了从模型到模型表单在字段上的映射关系。通常，这是没有什么问题，直接使用，按默认的来就行了。但是，有时候可能这种默认映射关系不是我们想要的，或者想进行一些更加灵活的定制，那怎么办呢？

**使用Meta类内部的widgets属性！**

`widgets`属性接收一个数据字典。其中每个元素的键必须是模型中的字段名之一，键值就是我们要自定义的内容了，具体格式和写法，参考下面的例子。
例如，如果你想要让Author模型中的name字段的类型从`CharField`更改为`<textarea>`，而不是默认的`<input type="text">`，可以如下重写字段的`Widget`：
```python
from django.forms import ModelForm, Textarea
from myapp.models import Author

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}), # 关键是这一行
        }
```
上面还展示了添加样式参数的格式。

如果你希望进一步自定义字段，还可以指定`Meta`类内部的`error_messages`、`help_texts`和`labels`属性，比如：
```python
from django.utils.translation import ugettext_lazy as _

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        labels = {
            'name': _('Writer'),
        }
        help_texts = {
            'name': _('Some useful help text.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }
```
还可以指定`field_classe`s属性将字段类型设置为你自己写的表单字段类型。
例如，如果你想为`slug`字段使用`MySlugFormField`，可以像下面这样：
```python
from django.forms import ModelForm
from myapp.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']
        field_classes = {
            'slug': MySlugFormField,
        }
```
最后，如果你想完全控制一个字段,包括它的类型，验证器，是否必填等等。可以显式地声明或指定这些性质，就像在普通表单中一样。比如，如果想要指定某个字段的验证器，可以显式定义字段并设置它的`validators`参数：
```python
from myapp.models import Article

class ArticleForm(ModelForm):
    slug = CharField(validators=[validate_slug])

    class Meta:
        model = Article
        fields = ['pub_date', 'headline', 'content', 'reporter', 'slug']
```

### 启用字段本地化

默认情况下，`ModelForm`中的字段不会本地化它们的数据。可以使用`Meta`类的`localized_fields`属性来启用字段的本地化功能。
```python
>>> from django.forms import ModelForm
>>> from myapp.models import Author
>>> class AuthorForm(ModelForm):
...     class Meta:
...         model = Author
...         localized_fields = ('birth_date',)
```
如果`localized_fields`设置为`__all__`这个特殊的值，所有的字段都将本地化。

### 表单的继承

`ModelForms`是可以被继承的。子模型表单可以添加额外的方法和属性，比如下面的例子：
```python
>>> class EnhancedArticleForm(ArticleForm):
...     def clean_pub_date(self):
...         ...
```
以上创建了一个`ArticleForm`的子类`EnhancedArticleForm`，并增加了一个`clean_pub_date`方法。

还可以修改`Meta.fields`或`Meta.exclude`列表，只要继承父类的`Meta`类，如下所示：
```python
>>> class RestrictedArticleForm(EnhancedArticleForm):
...     class Meta(ArticleForm.Meta):
...         exclude = ('body',)
```

### 提供初始值

可以在实例化一个表单时通过指定initial参数来提供表单中数据的初始值。
```python
>>> article = Article.objects.get(pk=1)
>>> article.headline
'My headline'
>>> form = ArticleForm(initial={'headline': 'Initial headline'}, instance=article)
>>> form['headline'].value()
'Initial headline'
```
## 文件上传

文件上传是网站开发中非常常见的功能。这里详细讲述如何在`Django`中实现文件的上传功能。

### 前端HTML代码实现

1. 在前端中，我们需要填入一个`form`标签，然后在这个`form`标签中指定`enctype="multipart/form-data"`，不然就不能上传文件。
2. 在`form`标签中添加一个`input`标签，然后指定`input`标签的`name`，以及`type="file"`。
以下两步的示例代码如下：
```html
    <form action="" method="post" enctype="multipart/form-data">
        <input type="file" name="myfile" />
    </form>
```

### 后端的代码实现

后端的主要工作是接收文件。然后存储文件，接收文件的方式跟接收`POST`的方式是一样的，只不过是通过`FILES`来实现。示例如下：
```python
    dev save_file(file):
        with open('somefile.txt','wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
                
    def index(request):
        if request.method == 'GET':
            form = MyForm()
            return render(request,'index.html',{'form':form})
        else:
            myfile = request.FILES.get('myfile')
            save_file(myfile)
            return HttpResponse('Success')
```
以上代码通过`request.FILES`接收到文件后，再写入到指定的地方。这样就可以完成一个文件的上传功能了。


### 使用模型来处理上传的文件

在定义模型的时候，我们可以给存储文件字段指定为`FileField`，这个`Field`可以传递一个`upload_to`参数，用来指定上传上来的文件保存到哪里。比如我们让他保存到项目的`files`目录下，示例代码如下：
```python
    # models.py
    
    class Article(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        thumbnail = models.FileField(upload_to='files')
        
    # views.py
    
    def index(request):
        if request.method == 'GET':
            return render(request,'index.html')
        else:
            title = request.POST.get('title')
            content = request.POST.get('content')
            thumbnail = request.FILES.get('thumbnail')
            article = Article(title=title,content=content,thumbnail=thumbnail)
            article.save()
```
调用完`article.save()`方法，就会把文件保存到`files`目录下面，并且会将这个文件的路径存储到数据库中。

### 指定`MEDIA_ROOT`和`MEDIA_URL`

以上我们是使用了`upload_to`来指定上传的文件的目录。我们也可以指定`MEDIA_ROOT`,就不需要在`FileField`中指定`upload_to`，他会自动的将文件上传到`MEDIA_ROOT`的目录下。
```python
    MEDIA_ROOT = os.path.join(BASE_DIR,'media')
    MEDIA_URL = '/media/'
```
然后我们可以在`urls.py`中添加`MEDIA_ROOT`目录下的访问路径。示例代码如下：
```python
    from django.urls import path
    from front import views
    from django.conf.urls.static import static
    from django.conf import settings
    
    urlpatterns = [
        path('',views.index),
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```
如果我们同时指定`MEDIA_ROOT`和`upload_to`，那么会将文件上传到`MEDIA_ROOT`下的`upload_to`目录中。示例代码如下：
```python
    class Article(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        thumbnail = models.FileField(upload_to="%Y/%m/%d/")
```

### 限制上传的文件扩展名

如果想限制上传的文件的扩展名，那么我们就需要用到表单来进行限制。我们可以使用普通的`Form`表单，也可以使用`ModelForm`，直接从模型中读取字段。示例代码如下：
```python
    # models.py
    class Article(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        thumbnial = models.FileField(upload_to='%Y/%m/%d/',validators=validators[validators.FileExtensionValidator(['txt','pdf'])])

    # forms.py
    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = "__all__"
```

### 上传图片

上传图片跟上传普通文件是一样的。只不过是上传图片的时候`Django`会判断上传的文件是否是图片的格式（除了判断后缀名，还会判断是否是可用的图片）。如果不是，那么就会验证失败。我们首先先来定义一个包含`ImageField`的模型。示例代码如下：
```python
    class Article(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        thumbnail = models.ImageField(upload_to="%Y/%m/%d/")
```
因为要验证是否是合格的图片，因此我们还需要用一个表单来进行验证。表单我们直接就使用`ModelForm`就可以了。示例代码如下：
```python
    class MyForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = "__all__"
```
**注意：使用ImageField，必须要先安装Pillow库：pip install pillow**

## Django表单API详解

---

声明：以下的`Form`、表单等术语都指的的广义的Django表单。

`Form`要么是绑定了数据的，要么是未绑定数据的。

如果是绑定的，那么它能够验证数据，并渲染表单及其数据，然后生成HTML表单。如果未绑定，则无法进行验证（因为没有数据可以验证！），但它仍然可以以HTML形式呈现空白表单。

表单类原型：class Form

若要创建一个未绑定的Form实例，只需简单地实例化该类：
```python
f = ContactForm()
```
若要绑定数据到表单，可以将数据以字典的形式传递给Form类的构造函数：
```python
    >>> data = {'subject': 'hello',
    ...         'message': 'Hi there',
    ...         'sender': 'foo@example.com',
    ...         'cc_myself': True}
    >>> f = ContactForm(data)
```
在这个字典中，键为字段的名称，它们对应于Form类中的字段。 值为需要验证的数据。

---

### 一、表单的绑定属性

**Form.is_bound：**
如果你需要区分绑定的表单和未绑定的表单，可以检查下表单的`is_bound`属性值：
```python
>>> f = ContactForm()
>>> f.is_bound
False
>>> f = ContactForm({'subject': 'hello'})
>>> f.is_bound
True
```
注意，传递一个空的字典将创建一个带有空数据的绑定的表单：
```python
>>> f = ContactForm({})
>>> f.is_bound
True
```
如果你有一个绑定的Form实例但是想改下数据，或者你想给一个未绑定的Form表单绑定某些数据，你需要创建另外一个Form实例。因为，Form实例的数据没是自读的，Form实例一旦创建，它的数据将不可变。

---

###  二、 使用表单验证数据

1. Form.clean()
如果你要自定义验证功能，那么你需要重新实现这个clean方法。

2. Form.is_valid()
调用is_valid()方法来执行绑定表单的数据验证工作，并返回一个表示数据是否合法的布尔值。
```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
True
```
让我们试下非法的数据。下面的情形中，subject为空（默认所有字段都是必需的）且sender是一个不合法的邮件地址：
```python
>>> data = {'subject': '',
...         'message': 'Hi there',
...         'sender': 'invalid email address',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
False
```

3. Form.errors
表单的errors属性保存了错误信息字典：
```python
>>> f.errors
{'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
```
在这个字典中，键为字段的名称，值为错误信息的Unicode字符串组成的列表。错误信息保存在列表中是因为字段可能有多个错误信息。

4. Form.errors.as_data()
返回一个字典，它将字段映射到原始的ValidationError实例。
```python
>>> f.errors.as_data()
{'sender': [ValidationError(['Enter a valid email address.'])],
'subject': [ValidationError(['This field is required.'])]}
```

5. Form.errors.as_json(escape_html=False)
返回JSON序列化后的错误信息字典。
```python
>>> f.errors.as_json()
{"sender": [{"message": "Enter a valid email address.", "code": "invalid"}],
"subject": [{"message": "This field is required.", "code": "required"}]}
```

6. Form.add_error(field, error)
向表单特定字段添加错误信息。

field参数为字段的名称。如果值为None，error将作为`Form.non_field_errors()`的一个非字段错误。

7. Form.has_error(field, code=None)
判断某个字段是否具有指定code的错误。当code为None时，如果字段有任何错误它都将返回True。

8. Form.non_field_errors()
返回Form.errors中不是与特定字段相关联的错误。

9. 对于没有绑定数据的表单
验证没有绑定数据的表单是没有意义的，下面的例子展示了这种情况：
```python
>>> f = ContactForm()
>>> f.is_valid()
False
>>> f.errors
{}
```

---

### 三、检查表单数据是否被修改

1. Form.has_changed()
当你需要检查表单的数据是否从初始数据发生改变时，可以使用`has_changed()`方法。
```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data, initial=data)
>>> f.has_changed()
False
```
提交表单后，我们可以重新构建表单并提供初始值，进行比较：
```python
>>> f = ContactForm(request.POST, initial=data)
>>> f.has_changed()
```
如果request.POST与initial中的数据有区别，则返回True，否则返回False。

2. Form.changed_data
返回有变化的字段的列表。
```python
>>> f = ContactForm(request.POST, initial=data)
>>> if f.has_changed():
...     print("The following fields changed: %s" % ", ".join(f.changed_data))
```

---

### 四、访问表单中的字段

通过fileds属性访问表单的字段：
```python
>>> for row in f.fields.values(): print(row)
...
<django.forms.fields.CharField object at 0x7ffaac632510>
<django.forms.fields.URLField object at 0x7ffaac632f90>
<django.forms.fields.CharField object at 0x7ffaac3aa050>
>>> f.fields['name']
<django.forms.fields.CharField object at 0x7ffaac6324d0>
```
可以修改Form实例的字段来改变字段在表单中的表示：
```python
>>> f.as_table().split('\n')[0]
'<tr><th>Name:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
>>> f.fields['name'].label = "Username"
>>> f.as_table().split('\n')[0]
'<tr><th>Username:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
```
注意不要改变`base_fields`属性，因为一旦修改将影响同一个Python进程中接下来所有的ContactForm实例：
```python
>>> f.base_fields['name'].label = "Username"
>>> another_f = CommentForm(auto_id=False)
>>> another_f.as_table().split('\n')[0]
'<tr><th>Username:</th><td><input name="name" type="text" value="class" required /></td></tr>'
```

---

### 五、访问cleaned_data

Form.cleaned_data

Form类中的每个字段不仅负责验证数据，还负责将它们转换为正确的格式。例如，`DateField`将输入转换为Python的`datetime.date`对象。无论你传递的是普通字符串'1994-07-15'、`DateField`格式的字符串、`datetime.date`对象、还是其它格式的数字，Django将始终把它们转换成`datetime.date`对象。

一旦你创建一个Form实例并通过验证后，你就可以通过它的cleaned_data属性访问干净的数据：
```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
```
如果你的数据没有通过验证，cleaned_data字典中只包含合法的字段：
```python
>>> data = {'subject': '',
...         'message': 'Hi there',
...         'sender': 'invalid email address',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
False
>>> f.cleaned_data
{'cc_myself': True, 'message': 'Hi there'}
```
`cleaned_data`字典始终只包含Form中定义的字段，即使你在构建Form时传递了额外的数据。 在下面的例子中，我们传递了一组额外的字段给ContactForm构造函数，但是`cleaned_data`将只包含表单的字段：
```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True,
...         'extra_field_1': 'foo',
...         'extra_field_2': 'bar',
...         'extra_field_3': 'baz'}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data # Doesn't contain extra_field_1, etc.
{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
```
当Form通过验证后，`cleaned_data`将包含所有字段的键和值，即使传递的数据中没有提供某些字段的值。 在下面的例子中，提供的实际数据中不包含`nick_name`字段，但是`cleaned_data`任然包含它，只是值为空：
```python
>>> from django import forms
>>> class OptionalPersonForm(forms.Form):
...     first_name = forms.CharField()
...     last_name = forms.CharField()
...     nick_name = forms.CharField(required=False)
>>> data = {'first_name': 'John', 'last_name': 'Lennon'}
>>> f = OptionalPersonForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}
```

---

### 六、表单的HTML生成方式

Form的第二个任务是将它渲染成HTML代码，默认情况下，根据form类中字段的编写顺序，在HTML中以同样的顺序罗列。 我们可以通过print方法展示出来：
```python
>>> f = ContactForm()
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```
如果表单是绑定的，输出的HTML将包含数据。
```python
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> f = ContactForm(data)
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" value="hello" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" value="Hi there" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" value="foo@example.com" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" checked /></td></tr>
```
注意事项：
+ 为了灵活性，输出不包含`<table>`和`</table>`、`<form>`和`</form`>以及`<input type="submit">`标签。 需要我们程序员手动添加它们。
+ 每个字段类型都由一个默认的HTML标签展示。注意，这些只是默认的，可以使用`Widget`特别指定。
+ 每个HTML标签的name属性名直接从ContactForm类中获取。
+ form使用HTML5语法，顶部需添加`<!DOCTYPE html>`说明。
    
1 . 渲染成文字段落`as_p()`
`Form.as_p()`

该方法将form渲染成一系列`<p`>标签，每个`<p>`标签包含一个字段；
```python
>>> f = ContactForm()
>>> f.as_p()
'<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>\n<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></p>\n<p><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" required /></p>\n<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>'
>>> print(f.as_p())
<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>
<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></p>
<p><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></p>
<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
```

2 . 渲染成无序列表`as_ul()`
`Form.as_ul()`

该方法将form渲染成一系列`<li>`标签，每个`<li>`标签包含一个字段。但不会自动生成`</ul>`和`<ul>`，所以你可以自己指定`<ul>`的任何HTML属性：
```python
>>> f = ContactForm()
>>> f.as_ul()
'<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></li>\n<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></li>\n<li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></li>\n<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>'
>>> print(f.as_ul())
<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required /></li>
<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required /></li>
<li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required /></li>
<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>
```

3 . 渲染成表格`as_table()`
`Form.as_table()`

渲染成HTML表格。它与print完全相同，事实上，当你print一个表单对象时，在后台调用的就是`as_table()`方法：
```python
>>> f = ContactForm()
>>> f.as_table()
'<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>\n<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>\n<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>\n<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>'
>>> print(f)
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```

---

### 七、 为错误信息添加CSS样式

Form.error_css_class

Form.required_css_class

为一些特别强调的或者需要额外显示的内容设置醒目的CSS样式是一种常用做法，也是非常有必要的。比如给必填字段加粗显示，设置错误文字为红色等等。
`Form.error_css_class`和`Form.required_css_class`属性就是做这个用的：
```python
from django import forms

class ContactForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    # ... and the rest of your fields here
```
属性名是固定的，不可变（废话），通过赋值不同的字符串，表示给这两类属性添加不同的CSS的class属性。以后Django在渲染form成HTML时将自动为error和required行添加对应的CSS样式。

上面的例子，其HTML看上去将类似：
```python
>>> f = ContactForm(data)
>>> print(f.as_table())
<tr class="required"><th><label class="required" for="id_subject">Subject:</label>    ...
<tr class="required"><th><label class="required" for="id_message">Message:</label>    ...
<tr class="required error"><th><label class="required" for="id_sender">Sender:</label>      ...
<tr><th><label for="id_cc_myself">Cc myself:<label> ...
>>> f['subject'].label_tag()
<label class="required" for="id_subject">Subject:</label>
>>> f['subject'].label_tag(attrs={'class': 'foo'})
<label for="id_subject" class="foo required">Subject:</label>
```

---

### 八、将上传的文件绑定到表单

处理带有FileField和ImageField字段的表单比普通的表单要稍微复杂一点。
首先，为了上传文件，你需要确保你的`<form>`元素定义`enctype`为`"multipart/form-data"`：
```html
<form enctype="multipart/form-data" method="post" action="/foo/">
```
其次，当你使用表单时，你需要绑定文件数据。文件数据的处理与普通的表单数据是分开的，所以如果表单包含FileField和ImageField，绑定表单时你需要指定第二个参数，参考下面的例子。
```python
# 为表单绑定image字段
>>> from django.core.files.uploadedfile import SimpleUploadedFile
>>> data = {'subject': 'hello',
...         'message': 'Hi there',
...         'sender': 'foo@example.com',
...         'cc_myself': True}
>>> file_data = {'mugshot': SimpleUploadedFile('face.jpg', <file data>)}
>>> f = ContactFormWithMugshot(data, file_data)
```
实际上，一般使用request.FILES作为文件数据的源：
```python
# Bound form with an image field, data from the request
>>> f = ContactFormWithMugshot(request.POST, request.FILES)
```
构造一个未绑定的表单和往常一样，将表单数据和文件数据同时省略：
```python
# Unbound form with an image field
>>> f = ContactFormWithMugshot()
```

## Django表单字段汇总

`Field.clean(value)`
虽然表单字段的Field类主要使用在Form类中，但也可以直接实例化它们来使用，以便更好地了解它们是如何工作的。每个Field的实例都有一个`clean()`方法，它接受一个参数，然后返回“清洁的”数据或者抛出一个`django.forms.ValidationError`异常：
```python
>>> from django import forms
>>> f = forms.EmailField()
>>> f.clean('foo@example.com')
'foo@example.com'
>>> f.clean('invalid email address')
Traceback (most recent call last):
...
ValidationError: ['Enter a valid email address.']
```
这个clean方法经常被我们用来在开发或测试过程中对数据进行验证和测试。

---

### 一、核心字段参数

以下的参数是每个Field类都可以使用的。

1 . **required**

给字段添加必填属性，不能空着。
```python
>>> from django import forms
>>> f = forms.CharField()
>>> f.clean('foo')
'foo'
>>> f.clean('')
Traceback (most recent call last):
...
ValidationError: ['This field is required.']
>>> f.clean(None)
Traceback (most recent call last):
...
ValidationError: ['This field is required.']
>>> f.clean(' ')
' '
>>> f.clean(0)
'0'
>>> f.clean(True)
'True'
>>> f.clean(False)
'False'
```

若要表示一个字段不是必需的，设置`required=False`：
```python
>>> f = forms.CharField(required=False)
>>> f.clean('foo')
'foo'
>>> f.clean('')
''
>>> f.clean(None)
''
>>> f.clean(0)
'0'
>>> f.clean(True)
'True'
>>> f.clean(False)
'False'
```

2 . **label**

label参数用来给字段添加‘人类友好’的提示信息。如果没有设置这个参数，那么就用字段的首字母大写名字。比如：

下面的例子，前两个字段有，最后的`comment`没有`labe`l参数：
```python
>>> from django import forms
>>> class CommentForm(forms.Form):
...     name = forms.CharField(label='Your name')
...     url = forms.URLField(label='Your website', required=False)
...     comment = forms.CharField()
>>> f = CommentForm(auto_id=False)
>>> print(f)
<tr><th>Your name:</th><td><input type="text" name="name" required /></td></tr>
<tr><th>Your website:</th><td><input type="url" name="url" /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>
```

3 . **label_suffix**

Django默认为上面的label参数后面加个冒号后缀，如果想自定义，可以使用label_suffix参数。比如下面的例子用“？”代替了冒号：
```python
>>> class ContactForm(forms.Form):
...     age = forms.IntegerField()
...     nationality = forms.CharField()
...     captcha_answer = forms.IntegerField(label='2 + 2', label_suffix=' =')
>>> f = ContactForm(label_suffix='?')
>>> print(f.as_p())
<p><label for="id_age">Age?</label> <input id="id_age" name="age" type="number" required /></p>
<p><label for="id_nationality">Nationality?</label> <input id="id_nationality" name="nationality" type="text" required /></p>
<p><label for="id_captcha_answer">2 + 2 =</label> <input id="id_captcha_answer" name="captcha_answer" type="number" required /></p>
```

4 . **initial**

为HTML页面中表单元素定义初始值。也就是input元素的value参数的值，如下所示：
```python
>>> from django import forms
>>> class CommentForm(forms.Form):
...     name = forms.CharField(initial='Your name')
...     url = forms.URLField(initial='http://')
...     comment = forms.CharField()
>>> f = CommentForm(auto_id=False)
>>> print(f)
<tr><th>Name:</th><td><input type="text" name="name" value="Your name" required /></td></tr>
<tr><th>Url:</th><td><input type="url" name="url" value="http://" required /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>
```
你可能会问为什么不在渲染表单的时候传递一个包含初始化值的字典给它，不是更方便？因为如果这么做，你将触发表单的验证过程，此时输出的HTML页面将包含验证中产生的错误，如下所示：
```python
>>> class CommentForm(forms.Form):
...     name = forms.CharField()
...     url = forms.URLField()
...     comment = forms.CharField()
>>> default_data = {'name': 'Your name', 'url': 'http://'}
>>> f = CommentForm(default_data, auto_id=False)
>>> print(f)
<tr><th>Name:</th><td><input type="text" name="name" value="Your name" required /></td></tr>
<tr><th>Url:</th><td><ul class="errorlist"><li>Enter a valid URL.</li></ul><input type="url" name="url" value="http://" required /></td></tr>
<tr><th>Comment:</th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="comment" required /></td></tr>
```
这就是为什么initial参数只用在未绑定的表单上。
还要注意，如果提交表单时某个字段的值没有填写，initial的值不会作为“默认”的数据。initial值只用于原始表单的显示：
```python
>>> class CommentForm(forms.Form):
...     name = forms.CharField(initial='Your name')
...     url = forms.URLField(initial='http://')
...     comment = forms.CharField()
>>> data = {'name': '', 'url': '', 'comment': 'Foo'}
>>> f = CommentForm(data)
>>> f.is_valid()
False
# The form does *not* fall back to using the initial values.
>>> f.errors
{'url': ['This field is required.'], 'name': ['This field is required.']}
```
除了常量之外，你还可以传递一个可调用的对象：
```python
>>> import datetime
>>> class DateForm(forms.Form):
...     day = forms.DateField(initial=datetime.date.today)
>>> print(DateForm())
<tr><th>Day:</th><td><input type="text" name="day" value="12/23/2008" required /><td></tr>
```

5 . **widget**

最重要的参数之一，指定渲染Widget时使用的widget类，也就是这个form字段在HTML页面中是显示为文本输入框？密码输入框？单选按钮？多选框？还是别的....

6 . **help_text**

该参数用于设置字段的辅助描述文本。
```python
>>> from django import forms
>>> class HelpTextContactForm(forms.Form):
...     subject = forms.CharField(max_length=100, help_text='100 characters max.')
...     message = forms.CharField()
...     sender = forms.EmailField(help_text='A valid email address, please.')
...     cc_myself = forms.BooleanField(required=False)
>>> f = HelpTextContactForm(auto_id=False)
>>> print(f.as_table())
<tr><th>Subject:</th><td><input type="text" name="subject" maxlength="100" required /><br /><span class="helptext">100 characters max.</span></td></tr>
<tr><th>Message:</th><td><input type="text" name="message" required /></td></tr>
<tr><th>Sender:</th><td><input type="email" name="sender" required /><br />A valid email address, please.</td></tr>
<tr><th>Cc myself:</th><td><input type="checkbox" name="cc_myself" /></td></tr>
>>> print(f.as_ul()))
<li>Subject: <input type="text" name="subject" maxlength="100" required /> <span class="helptext">100 characters max.</span></li>
<li>Message: <input type="text" name="message" required /></li>
<li>Sender: <input type="email" name="sender" required /> A valid email address, please.</li>
<li>Cc myself: <input type="checkbox" name="cc_myself" /></li>
>>> print(f.as_p())
<p>Subject: <input type="text" name="subject" maxlength="100" required /> <span class="helptext">100 characters max.</span></p>
<p>Message: <input type="text" name="message" required /></p>
<p>Sender: <input type="email" name="sender" required /> A valid email address, please.</p>
<p>Cc myself: <input type="checkbox" name="cc_myself" /></p>
```

7 . **error_messages**

该参数允许你覆盖字段引发异常时的默认信息。 传递的是一个字典，其键为你想覆盖的错误信息。 例如，下面是默认的错误信息：
```python
>>> from django import forms
>>> generic = forms.CharField()
>>> generic.clean('')
Traceback (most recent call last):
  ...
ValidationError: ['This field is required.']
```
而下面是自定义的错误信息：
```python
>>> name = forms.CharField(error_messages={'required': 'Please enter your name'})
>>> name.clean('')
Traceback (most recent call last):
  ...
ValidationError: ['Please enter your name']
```
可以指定多种类型的键，不仅仅针对‘requeired’错误，参考下面的内容。

8 . **validators**

指定一个列表，其中包含了为字段进行验证的函数。也就是说，如果你自定义了验证方法，不用Django内置的验证功能，那么要通过这个参数，将字段和自定义的验证方法链接起来。

9 . **localize**

localize参数帮助实现表单数据输入的本地化。

10 . **disabled**

设置有该属性的字段在前端页面中将显示为不可编辑状态。
该参数接收布尔值，当设置为True时，使用HTML的disabled属性禁用表单域，以使用户无法编辑该字段。即使非法篡改了前端页面的属性，向服务器提交了该字段的值，也将依然被忽略。

---

### Django表单内置的Field类

对于每个字段类，介绍其默认的widget，当输入为空时返回的值，以及采取何种验证方式。‘规范化为’表示转换为PYthon的何种对象。可用的错误信息键，表示该字段可自定义错误信息的类型（字典的键）。

1 . **BooleanField**

  + 默认的Widget：CheckboxInput
  + 空值：False
  + 规范化为：Python的True或者False
  + 可用的错误信息键：required
  
2 . **CharField**

  + 默认的Widget：TextInput
  + 空值：与empty_value给出的任何值。
  + 规范化为：一个Unicode 对象。
  + 验证max_length或min_length，如果设置了这两个参数。 否则，所有的输入都是合法的。
  + 可用的错误信息键：min_length, max_length, required
有四个可选参数：
  + max_length，min_length：设置字符串的最大和最小长度。
  + strip：如果True（默认），去除输入的前导和尾随空格。
  + empty_value：用来表示“空”的值。 默认为空字符串。
  
3 . **ChoiceField**

  + 默认的Widget：Select
  + 空值：''（一个空字符串）
  + 规范化为：一个Unicode 对象。
  + 验证给定的值是否在选项列表中。
  + 可用的错误信息键：required, invalid_choice
参数choices：用来作为该字段选项的一个二元组组成的可迭代对象（例如，列表或元组）或者一个可调用对象。格式与用于和ORM模型字段的choices参数相同。

4 . **TypedChoiceField**

像ChoiceField一样，只是还有两个额外的参数：coerce和empty_value。
  + 默认的Widget：Select
  + 空值：empty_value参数设置的值。
  + 规范化为：coerce参数类型的值。
  + 验证给定的值在选项列表中存在并且可以被强制转换。
  + 可用的错误信息的键：required, invalid_choice
  
5 . **DateField**

  + 默认的Widget：DateInput
  + 空值：None
  + 规范化为：datetime.date对象。
  + 验证给出的值是一个datetime.date、datetime.datetime 或指定日期格式的字符串。
  + 错误信息的键：required, invalid
  +接收一个可选的参数：input_formats。一个格式的列表，用于转换字符串为datetime.date对象。
如果没有提供input_formats，默认的输入格式为：
```python
['%Y-%m-%d',      # '2006-10-25'
 '%m/%d/%Y',      # '10/25/2006'
 '%m/%d/%y']      # '10/25/06'
```
另外，如果你在设置中指定`USE_L10N=False`，以下的格式也将包含在默认的输入格式中：
```python
['%b %d %Y',      # 'Oct 25 2006'
 '%b %d, %Y',     # 'Oct 25, 2006'
 '%d %b %Y',      # '25 Oct 2006'
 '%d %b, %Y',     # '25 Oct, 2006'
 '%B %d %Y',      # 'October 25 2006'
 '%B %d, %Y',     # 'October 25, 2006'
 '%d %B %Y',      # '25 October 2006'
 '%d %B, %Y']     # '25 October, 2006'
```

6 . **DateTimeField**

  + 默认的Widget：DateTimeInput
  + 空值：None
  + 规范化为：Python的datetime.datetime对象。
  + 验证给出的值是一个datetime.datetime、datetime.date或指定日期格式的字符串。
  + 错误信息的键：required, invalid
接收一个可选的参数：input_formats
如果没有提供input_formats，默认的输入格式为：
```python
['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
 '%Y-%m-%d',             # '2006-10-25'
 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
 '%m/%d/%Y',             # '10/25/2006'
 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
 '%m/%d/%y']             # '10/25/06'
```  

7 . **DecimalField**

  + 默认的Widget：当Field.localize是False时为NumberInput，否则为TextInput。
  + 空值：None
  + 规范化为：Python decimal对象。
  + 验证给定的值为一个十进制数。 忽略前导和尾随的空白。
  + 错误信息的键：max_whole_digits, max_digits, max_decimal_places,max_value, invalid, required,min_value
接收四个可选的参数：
  + max_value,min_value:允许的值的范围，需要赋值decimal.Decimal对象，不能直接给个整数类型。
  + max_digits：值允许的最大位数（小数点之前和之后的数字总共的位数，前导的零将被删除）。
  + decimal_places：允许的最大小数位。
  
8 . **DurationField**

  + 默认的Widget：TextInput
  + 空值：None
  + 规范化为：Python timedelta。
  + 验证给出的值是一个字符串，而且可以转换为timedelta对象。
  + 错误信息的键：required, invalid.
  
9 . **EmailField**

  + 默认的Widget：EmailInput
  + 空值：''（一个空字符串）
  + 规范化为：Unicode 对象。
  + 使用正则表达式验证给出的值是一个合法的邮件地址。
  + 错误信息的键：required, invalid
两个可选的参数用于验证，max_length 和min_length。  

10 . **FileField**

  + 默认的Widget：ClearableFileInput
  + 空值：None
  + 规范化为：一个UploadedFile对象，它封装文件内容和文件名到一个对象内。
  + 验证非空的文件数据已经绑定到表单。
  + 错误信息的键：missing, invalid, required, empty, max_length
具有两个可选的参数用于验证：max_length 和 allow_empty_file。

11 . **FilePathField**

  + 默认的Widget：Select
  + 空值：None
  + 规范化为：Unicode 对象。
  + 验证选择的选项在选项列表中存在。
  + 错误信息的键：required, invalid_choice
这个字段允许从一个特定的目录选择文件。 它有五个额外的参数，其中的`path`是必须的：
  + path：要列出的目录的绝对路径。 这个目录必须存在。
  + recursive：如果为False（默认值），只用直接位于path下的文件或目录作为选项。如果为True，将递归访问这个目录，其内所有的子目录和文件都将作为选项。
  + match：正则表达模式；只有具有与此表达式匹配的文件名称才被允许作为选项。
  + `allow_files`：可选。默认为True。表示是否应该包含指定位置的文件。它和`allow_folders`必须有一个为True。
  + `allow_folders`可选。默认为False。表示是否应该包含指定位置的目录。
  
12 . **FloatField**

  + 默认的Widget：当Field.localize是False时为NumberInput，否则为TextInput。
  + 空值：None
  + 规范化为：Float 对象。
  + 验证给定的值是一个浮点数。
  + 错误信息的键：max_value, invalid, required, min_value
接收两个可选的参数用于验证，max_value和min_value，控制允许的值的范围。

13 . **ImageField**

  + 默认的Widget：ClearableFileInput
  + 空值：None
  + 规范化为：一个UploadedFile对象，它封装文件内容和文件名为一个单独的对象。
  + 验证文件数据已绑定到表单，并且该文件是Pillow可以解析的图像格式。
  + 错误信息的键：missing, invalid, required, empty, invalid_image
使用ImageField需要安装Pillow（pip install pillow）。如果在上传图片时遇到图像损坏错误，通常意味着使用了Pillow不支持的格式。

14 . **IntegerField**

  + 默认的Widget：当Field.localize是False时为NumberInput，否则为TextInput。
  + 空值：None
  + 规范化为：Python 整数或长整数。
  + 验证给定值是一个整数。 允许前导和尾随空格，类似Python的int()函数。
  + 错误信息的键：max_value, invalid, required, min_value
两个可选参数：max_value和min_value，控制允许的值的范围。

15 . **GenericIPAddressField**

包含IPv4或IPv6地址的字段。
  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：一个Unicode对象。
  + 验证给定值是有效的IP地址。
  + 错误信息的键：required, invalid
有两个可选参数：protocol和unpack_ipv4

16 . **MultipleChoiceField**

  + 默认的Widget：SelectMultiple
  + 空值：[]（一个空列表）
  + 规范化为：一个Unicode 对象列表。
  + 验证给定值列表中的每个值都存在于选择列表中。
  + 错误信息的键：invalid_list, invalid_choice, required
  
17 . **TypedMultipleChoiceField**

类似MultipleChoiceField，除了需要两个额外的参数，coerce和empty_value。
  + 默认的Widget：SelectMultiple
  + 空值：empty_value
  + 规范化为：coerce参数提供的类型值列表。
  + 验证给定值存在于选项列表中并且可以强制。
  + 错误信息的键：required, invalid_choice
  
18 . **NullBooleanField**

  + 默认的Widget：NullBooleanSelect
  + 空值：None
  + 规范化为：Python None, False 或True 值。
  + 不验证任何内容（即，它从不引发ValidationError）。
  
19 . **RegexField**

  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：一个Unicode 对象。
  + 验证给定值与某个正则表达式匹配。
  + 错误信息的键：required, invalid
需要一个必需的参数：`regex`，需要匹配的正则表达式。
还可以接收max_length，min_length和strip参数，类似CharField。

20 . **SlugField**

  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：一个Unicode 对象。
  + 验证给定的字符串只包括字母、数字、下划线及连字符。
  + 错误信息的键：required, invalid
此字段用于在表单中表示模型的SlugField。

21 . **TimeField**

  + 默认的Widget：TextInput
  + 空值：None
  + 规范化为：一个Python 的datetime.time 对象。
  + 验证给定值是datetime.time或以特定时间格式格式化的字符串。
  + 错误信息的键：required, invalid
接收一个可选的参数：input_formats，用于尝试将字符串转换为有效的datetime.time对象的格式列表。

如果没有提供input_formats，默认的输入格式为：
```python
'%H:%M:%S',     # '14:30:59'
'%H:%M',        # '14:30'
```

22 . **URLField**

  + 默认的Widget：URLInput
  + 空值：''（一个空字符串）
  + 规范化为：一个Unicode 对象。
  + 验证给定值是个有效的URL。
  + 错误信息的键：required, invalid
可选参数：max_length和min_length

23 . **UUIDField**

  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：UUID对象。
  + 错误信息的键：required, invalid
  
24 . **ComboField**

  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：Unicode 对象。
  + 根据指定为ComboField的参数的每个字段验证给定值。
  + 错误信息的键：required, invalid
接收一个额外的必选参数：fields，用于验证字段值的字段列表（按提供它们的顺序）。
```python
>>> from django.forms import ComboField
>>> f = ComboField(fields=[CharField(max_length=20), EmailField()])
>>> f.clean('test@example.com')
'test@example.com'
>>> f.clean('longemailaddress@example.com')
Traceback (most recent call last):
...
ValidationError: ['Ensure this value has at most 20 characters (it has 28).']
```

25 . **MultiValueField**

  + 默认的Widget：TextInput
  + 空值：''（一个空字符串）
  + 规范化为：子类的compress方法返回的类型。
  + 根据指定为MultiValueField的参数的每个字段验证给定值。
  + 错误信息的键：incomplete, invalid, required
  
26 . **SplitDateTimeField**

  + 默认的Widget：SplitDateTimeWidget
  + 空值：None
  + 规范化为：Python datetime.datetime 对象。
  + 验证给定的值是datetime.datetime或以特定日期时间格式格式化的字符串。
  + 错误信息的键：invalid_date, invalid, required, invalid_time
  
---

### 三、创建自定义字段

如果内置的`Field`真的不能满足你的需求，还可以自定义`Field`。

只需要创建一个`django.forms.Field`的子类，并实现`clean(`)和`__init__()`构造方法。`__init__()`构造方法需要接收前面提过的那些核心参数，比如`widget、required,、label、help_text、initial`。

还可以通过覆盖`get_bound_field()`方法来自定义访问字段的方式。

## 表单的Widgets

不要将`Widget`与表单的`fields`字段混淆。表单字段负责验证输入并直接在模板中使用。而`Widget`负责渲染网页上HTML表单的输入元素和提取提交的原始数据。`widget`是字段的一个内在属性，用于定义字段在浏览器的页面里以何种HTML元素展现。

---

### 一、指定使用的widget

每个字段都有一个默认的widget类型。如果你想要使用一个不同的Widget，可以在定义字段时使用widget参数。 像这样：
```python
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
```
这将使用一个Textarea Widget来展现表单的评论字段，而不是默认的TextInput Widget。

---

### 二、设置widget的参数

许多`widget`具有可选的额外参数，下面的示例中，设置了`SelectDateWidget`的`years` 属性，注意参数的传递方法：
```python
from django import forms

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )
```

---

### 三、为widget添加CSS样式

默认情况下，当Django渲染Widget为实际的HTML代码时，不会帮你添加任何的CSS样式，也就是说网页上所有的TextInput元素的外观是一样的。

看下面的表单：
```python
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField()
```
这个表单包含三个默认的TextInput Widget，以默认的方式渲染，没有CSS类、没有额外的属性。每个Widget的输入框将渲染得一模一样，丑陋又单调：
```python
>>> f = CommentForm(auto_id=False)
>>> f.as_table()
<tr><th>Name:</th><td><input type="text" name="name" required /></td></tr>
<tr><th>Url:</th><td><input type="url" name="url" required /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>
```
在真正的网页中，你不想让每个Widget看上去都一样。可能想要给comment一个更大的输入框，可能想让`‘name’ Widget`具有一些特殊的CSS类。

可以在创建`Widge`t时使用`Widget.attrs`参数来实现这一目的：
```python
class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
    url = forms.URLField()
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
```
**注意参数的传递方式！**

这次渲染后的结果就不一样了：
```python
>>> f = CommentForm(auto_id=False)
>>> f.as_table()
<tr><th>Name:</th><td><input type="text" name="name" class="special" required /></td></tr>
<tr><th>Url:</th><td><input type="url" name="url" required /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" size="40" required /></td></tr>
```

