## 自定制Admin

如果只是在admin中简单的展示及管理模型，那么在admin.py模块中使用admin.site.register将模型注册一下就好了：
```python
from django.contrib import admin
from myproject.myapp.models import Author

admin.site.register(Author)
```
但是，很多时候这远远不够，我们需要对admin进行各种深度定制，以满足我们的需求。

这就要使用Django为我们提供的`ModelAdmin`类了。

`ModelAdmin`类是一个模型在admin页面里的展示方法，如果你对默认的admin页面满意，那么你完全不需要定义这个类，直接使用最原始的样子也行。通常，它们保存在app的admin.py文件里。下面是个简单的例子：
```python
from django.contrib import admin
from myproject.myapp.models import Author

# 创建一个ModelAdmin的子类
class AuthorAdmin(admin.ModelAdmin):
    pass

# 注册的时候，将原模型和ModelAdmin耦合起来
admin.site.register(Author, AuthorAdmin)
```

---

### 一、注册装饰器

除了常用的`admin.site.register(Author, AuthorAdmin)`方式进行注册，还可以用装饰器的方式连接模型和`ModelAdmin`。如下所示：
```python
from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
```
这个装饰器可以接收一些模型类作为参数，以及一个可选的关键字参数site（如果你使用的不是默认的AdminSite），比如。
```python
from django.contrib import admin
from .models import Author, Reader, Editor
from myproject.admin_site import custom_admin_site

@admin.register(Author, Reader, Editor, site=custom_admin_site)
class PersonAdmin(admin.ModelAdmin):
    pass
```

---

### 二、 搜索admin文件

当你在`INSTALLED_APPS`设置中添加了`django.contrib.admin`后，Django将自动在每个应用中搜索`admin`模块并导入它。也就是说，通常我们在每个`app`下都有一个`admin.py`文件，将当前`app`和`admin`有关的内容写到内部的`admin.py`文件中就可以了，Django会自动搜索并应用它们。
    + class apps.AdminConfig：admin默认的`AppConfig`类，当Django启动时自动调用其`autodiscover()`方法
    + class apps.SimpleAdminConfig：和上面的类似，但不调用`autodiscover()`
    + autodiscover()：自动搜索admin模块的方法。在使用自定义的site时，必须禁用这个方法，你应该在`INSTALLED_APPS`设置中用`django.contrib.admin.apps.SimpleAdminConfig`替代`django.contrib.admin`
    

---

### 三、ModelAdmin的属性

真正用来定制admin的手段，大部分都集中在这些ModelAdmin内置的属性上。
ModelAdmin非常灵活，它有许多内置属性，帮助我们自定义admin的界面和功能。所有的属性都定义在ModelAdmin的子类中，如下方式：
```python
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
```

1. ModelAdmin.actions
一个列表，包含自定义的actions，后面有专门的叙述。

2. ModelAdmin.actions_on_top
是否在列表上方显示actions的下拉框，默认为True

3. ModelAdmin.actions_on_bottom
是否在列表下方显示actions的下拉框，默认为False。效果看下面的图片，没什么大用途。
![](../images/chapter12/001.png)

4. ModelAdmin.actions_selection_counter
是否在actions下拉框右侧显示选中的对象的数量，默认为True，可改为False。
![](../images/chapter12/002.png)

5. ModelAdmin.date_hierarchy
根据你指定的日期相关的字段，为页面创建一个时间导航栏，可通过日期过滤对象。例如：
```python
date_hierarchy = 'pub_date'
```  
它的效果看起来是这样的：
![](../images/chapter12/003.png)

6. ModelAdmin.empty_value_display
指定空白显示的内容。如果你有些字段没有值（例如None，空字符串等等），默认情况下会显示破折号“-”。这个选项可以让你自定义显示什么，如下例就显示为`-empty-`：
```python
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
```
你还可以为整个admin站点设置默认空白显示值，通过设置`AdminSite.empty_value_display="xxxxxxx"`。甚至为某个函数设置空白值，如下：
```python
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'title', 'view_birth_date')

    def view_birth_date(self, obj):
        return obj.birth_date
    # 注意下面这句
    view_birth_date.empty_value_display = '???'
```

7 . ModelAdmin.exclude
不显示指定的某些字段。如下例有这么个模型：
```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3)
    birth_date = models.DateField(blank=True, null=True)
```
如果你不希望在页面内显示birth_date字段，那么这么设置：
```python
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'title')
```
和这么设置是一样的：
```python
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    # 一定注意了，值是个元组！一个元素的时候，最后的逗号不能省略。
    exclude = ('birth_date',)
```

8 . ModelAdmin.fields
按你希望的顺序，显示指定的字段。与`exclude`相对。但要注意与`list_display`区分。这里有个小技巧，你可以通过组合元组的方式，让某些字段在同一行内显示，例如下面的做法`url`和`title`将在一行内，而`content`则在下一行。
```python
class FlatPageAdmin(admin.ModelAdmin):
    fields = (('url', 'title'), 'content')
```
如果没有对`field`或`fieldsets`选项进行定义，那么Django将按照模型定义中的顺序，每一行显示一个字段的方式，逐个显示所有的非`AutoField`和`editable=True`的字段。（自动字段，如主键，不可编辑字段是不会出现在页面里的。）

9 . ModelAdmin.fieldsets
这个功能其实就是根据字段对页面进行分组显示或布局了。`fieldsets`是一个二元元组的列表。每个二元元组代表一个`<fieldset>`，是整个form的一部分。

二元元组的格式为(`name`,`field_options`)，`name`是一个表示该`filedset`标题的字符串，`field_options`是一个包含在该`filedset`内的字段列表。

下面是一个例子，有助于你理解：
```python
from django.contrib import admin

class FlatPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
```
它的页面看起来像下面的样子：
![](../images/chapter12/004.png)

在`filed_options`字典内，可以使用下面这些关键字：

**fields**：一个必填的元组，包含要在`fieldset`中显示的字段。例如：
```python
{
'fields': ('first_name', 'last_name', 'address', 'city', 'state'),
}
```
同样，它也可以像前面那样通过组合元组，实现多个字段在一行内的效果：
```pyhon
{
'fields': (('first_name', 'last_name'), 'address', 'city', 'state'),
}
```
`fileds`可以包含`readonly_fields`的值，作为只读字段。

**classes**：一个包含额外的CSS类的元组，例如：
```python
{
'classes': ('wide', 'extrapretty'),
}
```
两个比较有用的样式是collaspe和wide，前者将fieldsets折叠起来，后者让它具备更宽的水平空间。

**description**：一个可选的额外的说明文本，放置在每个`fieldset`的顶部。但是，这里并没有对`description`的HTML语法进行转义，因此可能有时候会造成一些莫名其妙的显示，要忽略HTML的影响，请使用`django.utils.html.escape()`手动转义。

10 . ModelAdmin.filter_horizontal
水平扩展多对多字段。默认情况下，`ManyTOManyField`在admin的页面中会显示为一个`select`框。在需要选择大量对象时，这会有点困难。将`ManyTOManyField`添加到这个属性列表里后，页面就会对字段进行扩展，并提供过滤功能。如下图：
![](../images/chapter12/005.png)

11 . ModelAdmin.filter_vertical
与上面的类似，不过是改成垂直布置了。

12 . ModelAdmin.form
默认情况下，admin系统会为你的模型动态的创建`ModelForm`，它用于创建你的添加/修改页面的表单。我们可以编写自定义的`ModelForm`，在"添加/修改"页面覆盖默认的表单行为。

注意：如果你的`ModelForm`和`ModelAdmin`同时定义了`exclude`选项，那么`ModelAdmin`中的具有优先权，如下例所示,"age"字段将被排除，但是“name”字段将被显示：
```python
from django import forms
from django.contrib import admin
from myapp.models import Person

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['name']

class PersonAdmin(admin.ModelAdmin):
    exclude = ['age']
    form = PersonForm
```

13 . ModelAdmin.formfield_overrides
这个属性比较难以理解，通过一个列子来解释可能会更好一点。设想一下我们自己写了个`RichTextEditorWidget`（富文本控件），然后想用它来代替传统的`<textarea>`（文本域控件）用于输入大段文字。我们可以这么做：
```python
from django.db import models
from django.contrib import admin

# 从对应的目录导入我们先前写好的widget和model
from myapp.widgets import RichTextEditorWidget
from myapp.models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RichTextEditorWidget},
    }
```
注意在上面的外层字典中的键是一个实际的字段类，而不是字符串，对应的值又是一个字典；这些参数将被传递给form字段的`__init__()`方法。

警告：如果你想使用一个带有关系字段的自定义`widget`。请确保你没有在`raw_id_fields`或`radio_fields`之中`include`那些字段的名字。

14 . ModelAdmin.inlines
参考`InlineModelAdmin`对象，就像`ModelAdmin.get_formsets_with_inlines()`一样。


### 三、ModelAdmin属性

15 . 指定显示在修改页面上的字段。这是一个很常用也是最重要的技巧之一。例如：
```python
list_display = ('first_name', 'last_name')
```
如果你不设置这个属性，admin站点将只显示一列，内容是每个对象的`__str__()`(Python2使用`__unicode__()`)方法返回的内容。

在list_display中，你可以设置四种值：
    + 模型的字段名
    ```python
    class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    ```
    + 一个函数，它接收一个模型实例作为参数
    ```python
    def upper_case_name(obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Name'

    class PersonAdmin(admin.ModelAdmin):
        list_display = (upper_case_name,)
    ```
    + 一个表示ModelAdmin的某个属性的字符串
    类似上面的函数调用，通过反射获取函数名，换了种写法而已，例如：
    ```python
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('upper_case_name',)

        def upper_case_name(self, obj):
            return ("%s %s" % (obj.first_name, obj.last_name)).upper()
        upper_case_name.short_description = 'Name'
    ```
    + 一个表示模型的某个属性的字符串
    类似第二种，但是此处的self是模型实例，引用的是模型的属性。参考下面的例子：
    ```python
    from django.db import models
    from django.contrib import admin
    
    class Person(models.Model):
        name = models.CharField(max_length=50)
        birthday = models.DateField()
    
        def decade_born_in(self):
            return self.birthday.strftime('%Y')[:3] + "0's"
        decade_born_in.short_description = 'Birth decade'
    
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('name', 'decade_born_in')
    ```
    下面是对list_display属性的一些特别提醒：
        + 对于Foreignkey字段，显示的将是其`__str__()`方法的值。
        + 不支持ManyToMany字段。如果你非要显示它，请自定义方法。
        + 对于BooleanField或NullBooleanField字段，会用on/off图标代替True/False。
        + 如果给list_display提供的值是一个模型的、ModelAdmin的或者可调用的方法，默认情况下会自动对返回结果进行HTML转义，这可能不是你想要的。
    下面是一个完整的例子：
    
    ```python
    from django.db import models
    from django.contrib import admin
    from django.utils.html import format_html
    
    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        color_code = models.CharField(max_length=6)
    
        def colored_name(self):
            # 关键是这句！！！！！请自己调整缩进。
            return '<span style="color: #%s;">%s %s</span>'%(
                self.color_code,
                self.first_name,
                self.last_name,
            )
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('first_name', 'last_name', 'colored_name')
    ```
    
    实际的效果如下图所示：
    ![](../images/chapter12/006.png)
    
    很明显，你是想要有个CSS效果，但Django把它当普通的字符串了。怎么办呢？用`format_html()`或者`format_html_join()`或者`mark_safe()`方法！
    
    ```python
    from django.db import models
    from django.contrib import admin
    # 需要先导入！
    from django.utils.html import format_html
    
    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        color_code = models.CharField(max_length=6)
    
        def colored_name(self):
            # 这里还是重点，注意调用方式，‘%’变成‘{}’了！
            return format_html(
                '<span style="color: #{};">{} {}</span>',
                self.color_code,
                self.first_name,
                self.last_name,
            )
    
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('first_name', 'last_name', 'colored_name')
    ```
    下面看起来就会是你想要的结果了：
    
    ![](../images/chapter12/007.png)
    
    + 如果某个字段的值为None或空字符串或空的可迭代对象，那么默认显示为短横杠“-”，你可以使用`AdminSite.empty_value_display`在全局改写这一行为：
    ```python
    from django.contrib import admin

    admin.site.empty_value_display = '(None)'
    ```
    或者使用`ModelAdmin.empty_value_display`只改变某个类的行为：
    ```python
    class PersonAdmin(admin.ModelAdmin):
        empty_value_display = 'unknown'
    ```
    或者更细粒度的只改变某个字段的这一行为：
    ```python
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('name', 'birth_date_view')
    
        def birth_date_view(self, obj):
             return obj.birth_date
    
        birth_date_view.empty_value_display = 'unknown'
    ```
    + 默认情况下，一个返回布尔值的方法在list_display中显示为True或者False的：
    ![](../images/chapter12/008.png)
    但如果你给这个方法添加一个boolean的属性并赋值为True，它将显示为on/off的图标，如下图：
    ```python
    from django.db import models
    from django.contrib import admin
    
    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        birthday = models.DateField()
    
        def born_in_fifties(self):
            return self.birthday.strftime('%Y')[:3] == '195'
        # 关键在这里
        born_in_fifties.boolean = True
    
    class PersonAdmin(admin.ModelAdmin):
        # 官方文档这里有错，将'name'改为'first_name' 
        list_display = ('first_name', 'born_in_fifties')
    ```
    ![](../images/chapter12/009.png)
    
    + 通常情况下，在list_display列表里的元素如果不是数据库内的某个具体字段，是不能根据它进行排序的。但是如果给这个字段添加一个admin_order_field属性，并赋值一个具体的数据库内的字段，则可以按这个字段对原字段进行排序，如下所示：
    ```python
    from django.db import models
    from django.contrib import admin
    from django.utils.html import format_html
    
    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        color_code = models.CharField(max_length=6)
    
        def colored_first_name(self):
            return format_html(
                '<span style="color: #{};">{}</span>',
                self.color_code,
                self.first_name,
            )
        # 就是这一句了！
        colored_first_name.admin_order_field = 'first_name'
    
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('first_name', 'colored_first_name')
    ```
    本来colored_first_name是不能排序的，给它的admin_order_field赋值first_name后，就依托first_name进行排序了。

    要降序的话，使用连字符“-”前缀：
    ```python
    colored_first_name.admin_order_field = '-first_name'
    ```
    还可以跨表跨关系引用：
    ```python
    class Blog(models.Model):
        title = models.CharField(max_length=255)
        author = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    class BlogAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'author_first_name')
    
        def author_first_name(self, obj):
            return obj.author.first_name
        # 指定了另一张表的first_name作为排序的依据
        author_first_name.admin_order_field = 'author__first_name'
    ```
    + list_display里的元素还可以是某个属性。但是请注意的是，如果使用python的@property方式来构造一个属性，则不能给它添加short_description描述，只有使用property()函数的方法构造属性的时候，才可以添加short_description描述，如下：
    ```python
    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
    
        def my_property(self):
            return self.first_name + ' ' + self.last_name
        my_property.short_description = "Full name of the person"
    
        full_name = property(my_property)
    
    class PersonAdmin(admin.ModelAdmin):
        list_display = ('full_name',)
    ```
    + list_display中的每个字段名在HTML中都将自动生成CSS类属性，在th标签中以column-<field_name>的格式，    
    + 你可以通过它，对前端进行自定义或调整，例如设置宽度等等。
    + Django将按下面的顺序，解释list_display中的每个元素：
    + 模型的字段
    + 可调用对象
    + ModelAdmin的属性
    + 模型的属性
    
16 . ModelAdmin.list_display_links
指定用于链接修改页面的字段。通常情况，list_display列表中的第一个元素被作为指向目标修改页面的超级链接点。但是，使用list_display_links可以帮你修改这一默认配置。
如果设置为None，则根本没有链接了，你无法跳到目标的修改页面。或者设置为一个字段的元组或列表（和list_display的格式一样），这里面的每一个元素都是一个指向修改页面的链接。你可以指定和list_display一样多的元素个数，Django不关系它的多少。唯一需要注意的是，如果你要使用list_display_links，你必须先有list_display。
下面这个例子中first_name和last_name都可以点击并跳转到修改页面。
```python
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday')
    list_display_links = ('first_name', 'last_name')
```
而如果这样，你将没有任何链接：
```python
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'message')
    list_display_links = None
```

17 . ModelAdmin.list_editable
这个选项是让你指定在修改列表页面中哪些字段可以被编辑。指定的字段将显示为编辑框，可修改后直接批量保存，如下图：
![](../images/chapter12/010.png)

在这里，我们将`last_name`设置为了`list_editable`。

需要注意的是：一是不能将`list_display`中没有的元素设置为`list_editable`，二是不能将`list_display_links`中的元素设置为`list_editable`。原因很简单，你不能编辑没显示的字段或者作为超级链接的字段。
### 三、ModelAdmin属性

18 . ModelAdmin.list_filter
设置`list_filter`属性后，可以激活修改列表页面的右侧边栏，用于对列表元素进行过滤，如下图：
![](../images/chapter12/011.png)

list_filter必须是一个元组或列表，其元素是如下类型之一：
    + 某个字段名，但该字段必须是BooleanField、CharField、DateField、DateTimeField、IntegerField、ForeignKey或者ManyToManyField中的一种。例如：
    ```python
    class PersonAdmin(admin.ModelAdmin):
        list_filter = ('is_staff', 'company')
    ```
    在这里，你可以利用双下划线进行跨表关联，如下例：
    ```python
    class PersonAdmin(admin.UserAdmin):
        list_filter = ('company__name',)
    ```
    
    + 一个继承django.contrib.admin.SimpleListFilter的类。你要给这个类提供title和parameter_name的值，并重写lookups和queryset方法。例如：
    
    ```python
    from datetime import date
    from django.contrib import admin
    from django.utils.translation import ugettext_lazy as _
    
    class DecadeBornListFilter(admin.SimpleListFilter):
        # 提供一个可读的标题
        title = _('出生年代')
    
        # 用于URL查询的参数.
        parameter_name = 'decade'
    
        def lookups(self, request, model_admin):
            """
            返回一个二维元组。每个元组的第一个元素是用于URL查询的真实值，
            这个值会被self.value()方法获取，并作为queryset方法的选择条件。
            第二个元素则是可读的显示在admin页面右边侧栏的过滤选项。        
            """
            return (
                ('80s', _('80年代')),
                ('90s', _('90年代')),
            )
            
        def queryset(self, request, queryset):
            """
            根据self.value()方法获取的条件值的不同执行具体的查询操作。
            并返回相应的结果。
            """
            if self.value() == '80s':
                return queryset.filter(birthday__gte=date(1980, 1, 1),
                                        birthday__lte=date(1989, 12, 31))
            if self.value() == '90s':
                return queryset.filter(birthday__gte=date(1990, 1, 1),
                                        birthday__lte=date(1999, 12, 31))

    class PersonAdmin(admin.ModelAdmin):
    
        list_display = ('first_name', 'last_name', "colored_first_name",'birthday')
    
        list_filter = (DecadeBornListFilter,)
    ```
    其效果如下图：
    ![](../images/chapter12/012.png)
    注意：为了方便，我们通常会将HttpRequest对象传递给lookups和queryset方法，如下所示：
    ```python
    class AuthDecadeBornListFilter(DecadeBornListFilter):

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return super(AuthDecadeBornListFilter, self).lookups(request, model_admin)

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return super(AuthDecadeBornListFilter, self).queryset(request, queryset)
    ```
    同样的，我们默认将ModelAdmin对象传递给lookups方法。下面的例子根据查询结果，调整过滤选项，如果某个年代没有符合的对象，则这个选项不会在右边的过滤栏中显示：
    ```python
    class AdvancedDecadeBornListFilter(DecadeBornListFilter):

    def lookups(self, request, model_admin):
        """
        只有存在确切的对象，并且它出生在对应年代时，才会出现这个过滤选项。
        """
        qs = model_admin.get_queryset(request)
        if qs.filter(birthday__gte=date(1980, 1, 1),
                      birthday__lte=date(1989, 12, 31)).exists():
            yield ('80s', _('in the eighties'))
        if qs.filter(birthday__gte=date(1990, 1, 1),
                      birthday__lte=date(1999, 12, 31)).exists():
            yield ('90s', _('in the nineties'))
    ```
    + 也可以是一个元组。它的第一个元素是个字段名，第二个元素则是继承了django.contrib.admin.FieldListFilter的类。例如：
    ```python
    class PersonAdmin(admin.ModelAdmin):
        list_filter = (
            ('is_staff', admin.BooleanFieldListFilter),
        )
    ```
    你可以使用RelatedOnlyFieldListFilter限制关联的对象。假设author是关联User模型的ForeignKey，下面的用法将只选择那些出过书的user而不是所有的user：
    ```python
    class BookAdmin(admin.ModelAdmin):
        list_filter = (
            ('author', admin.RelatedOnlyFieldListFilter),
        )
    ```
    另外，其template属性可以指定渲染的模板，如下则指定了一个自定义的模板。（Django默认的模板为admin/filter.html）
    ```python
    class FilterWithCustomTemplate(admin.SimpleListFilter):
        template = "custom_template.html"
    ```

19 . ModelAdmin.list_max_show_all
设置一个数值，当列表元素总数小于这个值的时候，将显示一个“show all”链接，点击后就能看到一个展示了所有元素的页面。该值默认为200.

20 . ModelAdmin.list_per_page
设置每页显示多少个元素。Django自动帮你分页。默认为100。

21 . ModelAdmin.list_select_related
如果设置了`list_select_related`属性，Django将会使用`select_related()`方法查询数据，这可能会帮助你减少一些数据库访问。

属性的值可以是布尔值、元组或列表，默认为False。当值为True时，将始终调用`select_related()`方法；如果值为False，Django将查看`list_display`属性，只对`ForeignKey`字段调用`select_related()`方法。
如果你需要更细粒度的控制，请赋值一个元组（或列表）。空元组将阻止`select_related()`方法，否则元组会被当做参数传递给`select_related()`方法。例如：
```python
class ArticleAdmin(admin.ModelAdmin):
    list_select_related = ('author', 'category')
```
这将会调用`select_related('author', 'category')`。

22 . ModelAdmin.ordering
设置排序的方式。

属性的值必须为一个元组或列表，格式和模型的ordering参数一样。如果不设置这个属性，Django将按默认方式进行排序。如果你想进行动态排序，请自己实现`get_ordering()`方法。

23 . ModelAdmin.paginator
指定用于分页的分页器。默认情况下，分页器用的是Django自带的`django.core.paginator.Paginato`r。如果自定义分页器的构造函数接口和`django.core.paginator.Paginator`的不一样，那你还需要自己实现`ModelAdmin.get_paginator()`方法。

24 . ModelAdmin.prepopulated_fields
设置预填充字段。不接收DateTimeField、ForeignKey和ManyToManyField类型的字段。
```python
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
```

25 . ModelAdmin.preserve_filters
默认情况下，当你对目标进行创建、编辑或删除操作后，页面会依然保持原来的过滤状态。将preserve_filters设为False后，则会返回未过滤状态。

26 . ModelAdmin.radio_fields
默认情况下，Django使用select标签显示ForeignKey或choices集合。如果将这种字段设置为radio_fields，则会以radio_box标签的形式展示。下面的例子假设group是Person模型的ForeignKey字段，
```python
class PersonAdmin(admin.ModelAdmin):
    # 垂直布局。（肯定也有水平布局HORIZONTAL的啦）
    radio_fields = {"group": admin.VERTICAL}
```
注意：不要将ForeignKey或choices集合之外的字段类型设置给这个属性。
![](../images/chapter12/013.png)

27 . ModelAdmin.raw_id_fields
这个属性会改变默认的`ForeignKey`和`ManyToManyField`的展示方式，它会变成一个输入框，用于输入关联对象的主键id。对于`ManyToManyField`，id以逗号分隔。并且再输入框右侧提供一个放大镜的图标，你可以点击进入选择界面。例如：
```python
class PersonAdmin(admin.ModelAdmin):
    raw_id_fields = ("group",)
```
![](../images/chapter12/014.png)

28 . ModelAdmin.readonly_fields
该属性包含的字段在页面内将展示为不可编辑状态。它还可以展示模型或者ModelAdmin本身的方法的返回值，类似`ModelAdmin.list_display`的行为。参考下面的例子：
```python
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('address_report',)

    def address_report(self, instance):
        # assuming get_full_address() returns a list of strings
        # for each line of the address and you want to separate each
        # line by a linebreak
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line,) for line in instance.get_full_address()),
        ) or mark_safe("<span class='errors'>I can't determine this address.</span>")

    # short_description functions like a model field's verbose_name
    address_report.short_description = "Address"
```
29 . ModelAdmin.save_as
默认情况下，它的值为False。如果设置为True，那么右下角的“Save and add another”按钮将被替换成“Save as new”，意思也变成保存为一个新的对象。
![](../images/chapter12/015.png)

30 . ModelAdmin.save_as_continue
默认值为True, 在保存新对象后跳转到该对象的修改页面。但是如果这时save_as_continue=False，则会跳转到元素列表页面。

31 . ModelAdmin.save_on_top
默认为False。 设为True时，页面的顶部会提供同样的一系列保存按钮。

32 . ModelAdmin.search_fields
设置这个属性，可以为admin的修改列表页面添加一个搜索框
![](../images/chapter12/016.png)
被搜索的字段可以是`CharField`或者`TextField`文本类型，也可以通过双下划线进行`ForeignKey`或者`ManyToManyField`的查询，格式为`search_fields = ['foreign_key__related_fieldname']`.

例如：如果作者是博客的`ForeignKey`字段，下面的方式将通过作者的email地址来查询对应的博客，也就是email地址是查询值的作者所写的所有博客。
```python
search_fields = ['user__email']
```
当你在搜索框里输入一些文本的时候，Django会将文本分割成一个一个的关键字，并返回所有包含这些关键字的对象，必须注意的是，每个关键词至少得是`search_fields`其中之一。例如，如果`search_fields`是`['first_name', 'last_name']`，当用户输入`John lennon`时（注意中间的空格），Django将执行等同于下面的SQL语法WHERE子句：
```sql
WHERE (first_name ILIKE '%john%' OR last_name ILIKE '%john%') AND (first_name ILIKE '%lennon%' OR last_name ILIKE '%lennon%')
```
如果要执行更加严格的匹配或搜索，可以使用一些元字符，例如“^”。类似正则，它代表从开头匹配。例如，如果`search_fields`是`['^first_name','^last_name']`,当用户输入“`John lennon`”时（注意中间的空格），Django将执行等同于下面的SQL语法WHERE子句：
```sql
WHERE (first_name ILIKE 'john%' OR last_name ILIKE 'john%') AND (first_name ILIKE 'lennon%' OR last_name ILIKE 'lennon%')
```
也可以使用“=”，来进行区分大小写的并绝对相等的严格匹配。例如，如果`search_fields`是`['=first_name','=last_name']`,当用户输入“`John lennon`”时（注意中间的空格），Django将执行等同于下面的SQL语法WHERE子句：
```sql
WHERE (first_name ILIKE 'john' OR last_name ILIKE 'john') AND (first_name ILIKE 'lennon' OR last_name ILIKE 'lennon')
```

33 . ModelAdmin.show_full_result_count
用于设置是否显示一个过滤后的对象总数的提示信息，例如“99 results (103 total)”。如果它被设置为False，那么显示的将是“ 99 results (Show all)”。 默认情况下，它的值为True，这将会对整个表进行一个count操作，在表很大的时候，可能会耗费一定的时间和资源。

34 . ModelAdmin.view_on_site
这个属性可以控制是否在admin页面显示`View site`的链接。这个链接主要用于跳转到你指定的URL页面。
![](../images/chapter12/017.png)

属性的值可以是布尔值或某个调用。如果是True（默认值），对象的`get_absolute_url()`方法将被调用并生成rul。
如果你的模型有一个`get_absolute_url()`方法，但你不想显示“`View site`”链接，你只需要将`view_on_site`属性设置为False。
```python
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    view_on_site = False
```
如果属性的值是一个调用，它将接收一个模型实例作为参数：
```python
from django.contrib import admin
from django.urls import reverse

class PersonAdmin(admin.ModelAdmin):
    def view_on_site(self, obj):
        url = reverse('person-detail', kwargs={'slug': obj.slug})
        return 'https://example.com' + url
```

## 自定义Admin actions

通常情况下，admin的工作模式是“选中目标，然后修改目标”，但在同时修改大量目标的时候，这种模式就变得重复、繁琐。

为此，admin提供了自定义功能函数actions的手段，可以批量对数据进行修改。admin内置了一个批量删除对象的操作，如下图所示：
![](../images/chapter12/018.png)
下面以一个新闻应用的文章模型为例，介绍一个批量更新的自定义actions，它将选择的文章由“草稿”状态更新为“发布”状态：

首先是模型的代码：
```python
from django.db import models

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):              # __unicode__ on Python 2
        return self.title
```

---

### 编写action

action必须携带三个参数：
    + 当前的ModelAdmin
    + 当前的HttpRequest对象（即request）
    + 被选择的对象（即QuerySet）
    
在应用中的admin.py文件中写入：
```python
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
```
注意：这里我们作为例子，简单地使用了queryset自带的update()方法，它能批量操作。但在多数情况下，你要自己遍历queryset的每个元素，并编写具体的操作。也就是：
```python
for obj in queryset:
    do_something_with(obj)
```
还可以设置一个简单易懂的简短描述(可以使用中文)，用于代替生硬的函数名：
```python
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
# 注意缩进，下面这句不在函数体内。
make_published.short_description = "Mark selected stories as published"
```

---

### 将自定义action添加到对应的ModelAdmin中

关键是其中的`actions = [make_published]`这句。
```python
from django.contrib import admin
from myapp.models import Article

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Article, ArticleAdmin)
```
然后，页面看起来是下面的样子（注意下拉框）：
![](../images/chapter12/019.png)

处理错误：

这其中，如果你能够预知在自定义的操作中可能产生的错误，请处理该错误，并通过django.contrib.admin.ModelAdmin.message_user()以友好的方式给予用户提示信息。

---

### 三、将action定义为ModelAdmin的方法

上面的make_published看起来已经不错了，但是我们一般会将它作为ModelAdmin的方法来使用。下面我们把它移到ArticleAdmin类中：
```python
class ArticleAdmin(admin.ModelAdmin):
    ...

    actions = ['make_published']  # 请注意这里改成字符串引用了
    # 第一个参数变为self
    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "Mark selected stories as published"
```
这样做的好处是自定义方法可以直接访问类本身。例如下面使用self引用，为方法添加提示信息的功能：
```python
class ArticleAdmin(admin.ModelAdmin):
    ...

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
```
回到浏览器，再试试，你会看到如下图所示（注意顶部的绿色提示行）：
![](../images/chapter12/020.png)


---

### 四、跳转到中间页面

默认情况下，执行完actions后，浏览器会返回先前的修改列表页面。但有时候，一些复杂的action需要返回中间页面，例如内置的删除方法，在执行删除动作之前，会弹出一个删除确认页面。

要实现这个功能，只需要在action方法中返回一个HttpResponse（或它的子类）。 例如下面是一个利用Django内置的序列化函数将一个对象保存为json格式的范例：
```python
from django.http import HttpResponse
from django.core import serializers

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response
```
多数情况下，我们会使用HttpResponseRedirect跳转到一个中间页面，并在GET方法的url中携带别选择的对象作为参数传递过去，然后在这个新的视图中接收这个参数，并编写具体的更加复杂的业务逻辑，如下面的代码所示：
```python
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryset):
    # 获得被打钩的checkbox对应的对象
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    # 获取对应的模型
    ct = ContentType.objects.get_for_model(queryset.model)
    # 构造访问的url，使用GET方法，跳转到相应的页面
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
```
具体的业务views这里没有给出，作为练习，留给大家。

---

### 五、编写可用于整个admin站点的action

前面创建的actions智能应用于绑定的模型。实际上有时候，我们还需要可以对admin站点内所有模型都有效的acitons。上面写的`export_selected_objects`函数可以是一个很好的例子。要实现这一功能，你需要使用内置的`AdminSite.add_action`方法：`AdminSite.add_action(action, name=None)`
```python
from django.contrib import admin

admin.site.add_action(export_selected_objects)
```

---

### 六、禁用acitons

有时候，对于某些actions，我们想全局禁用或者局部禁用它。需要使用AdminSite.disable_action(name)方法。
    + 禁用全站级别的acitons：
例如，禁用内置的删除方法：
```python
admin.site.disable_action('delete_selected')
```
    + 全站禁用，但个别可用：在ModelAdmin.actions中显式地引用。
例如：
```python
# 全站禁用删除功能
admin.site.disable_action('delete_selected')

# 这个老老实实的被禁了
class SomeModelAdmin(admin.ModelAdmin):
    actions = ['some_other_action']
    ...

# 这个声明：我还要用
class AnotherModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected', 'a_third_action']
    ...
```
    + 在指定模型中禁用所有actions：设置ModelAdmin.actions为None。（这会连带全局actions一起禁用了。）
    ```python
    class MyModelAdmin(admin.ModelAdmin):
        actions = None
    ```
    + 根据条件自动启用或禁用
    还可以根据条件自动选择性的启动或禁用某些acitons，你只需要改写ModelAdmin.get_actions()方法。该方法将返回一个包含actions的字典。字典的键是aciton的名字（也就是前面的'delete_selected', 'a_third_action'之类），值是一个元组，包含（函数、名字、别名）例如，允许用户名以“J”开头的用户批量删除对象，但其它用户不行：
    ```python
    class MyModelAdmin(admin.ModelAdmin):
    ...

    def get_actions(self, request):
        actions = super(MyModelAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions
    ```

    ## Admin文档生成器

Django的admindocs应用可以从模型、视图、模板标签等地方获得文档内容。

---

### 一、概览
要激活admindocs，请按下面的步骤操作：
    + 在`INSTALLED_APPS`内添加`django.contrib.admindocs`
    + 在`urlpatterns`内添加url(r'^admin/doc/',include('django.contrib.admindocs.urls'))。确保它处于r'^admin/'条目之前，原因你懂的。
    + 安装Python的docutils模块(http://docutils.sf.net/)(pip3 install docutils)
    + 可选：想使用admindocs的书签小工具，需要安装django.contrib.admindocs.middleware.XViewMiddleware。
    
如果上述步骤顺利完成，那么你可以从admin界面访问doc界面，也可以直接访问/admin/doc，如下图：
![](../images/chapter12/021.png)
它看起来是下面的样子：
![](../images/chapter12/022.png)
下面的这些特殊标记，可帮助你在文档字符串中，快速创建指向其它组件的链接：
![](../images/chapter12/023.jpg)

---

### 二、模型

在doc页面的模型部分，列出了所有的模型，点击可以查看具体的字段等细节信息。信息主要来自字段的help_txt部分和模型方法的docstring部分。如下面图中展示：

有用的帮助信息看起来是这个样子的：
```python
class BlogEntry(models.Model):
    """
    Stores a single blog entry, related to :model:`blog.Blog` and
    :model:`auth.User`.
    """
    slug = models.SlugField(help_text="A short label, generally used in URLs.")
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True, null=True,
    )
    blog = models.ForeignKey(Blog, models.CASCADE)
    ...

    def publish(self):
        """Makes the blog entry live on the site."""
        ...
```
![](../images/chapter12/024.png)
![](../images/chapter12/025.png)

---

### 三、视图

站点内的每个URL都会在doc内享有一个页面，点击某个URL将会展示对应的视图信息。主要包括下面这些信息，请尽量丰富它们：
    + 视图功能的简单描述
    + 下文环境，或者视图模块里的变量列表
    + 视图内使用的模板
    
例如：
```python
from django.shortcuts import render

from myapp.models import MyModel

def my_view(request, slug):
    """
    Display an individual :model:`myapp.MyModel`.

    **Context**

    ``mymodel``
        An instance of :model:`myapp.MyModel`.

    **Template:**

    :template:`myapp/my_template.html`
    """
    context = {'mymodel': MyModel.objects.get(slug=slug)}
    return render(request, 'myapp/my_template.html', context)
```
![](../images/chapter12/026.png)

---

### 四、模板标签和过滤器

所有Django内置的或者你自定义的或者第三方app提供的标签和过滤器都将在页面内展示：
![](../images/chapter12/027.png)
![](../images/chapter12/028.png)

