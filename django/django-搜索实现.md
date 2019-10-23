# 在django项目中实现搜索的功能

## 使用原生mysql的模糊查找来实现 

通过orm来操作模型来获取相关数据的模型，然后通过`context`参数将数据传到模版中，在模版中将查找到的数据进行渲染，就可以了
这种方式适用于数据量比较小的站内搜索。如果数据量很大的话，那么就可以是使用搜索引擎来实现。
例如我们要查询新闻的标题和内容的关键字，那么示例代码如下：

1. 配置搜索的url
```python
from django.urls import path
from . import views 
urlpatterns = [
    path("search/",views.search,name="search")
]
```
2. 视图
```python 
form django.db.models import Q
def search(request):
    q = request.GET.get("q")
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context["newses"] = newses
    return render(request,"search.html",context=context)
```
3. 在模版中就使用for循环将查找到的新闻遍历展示出来就可以了
```html
{% for news in newses%}
    {{ news.name}}
    ....
{% endfor%}
```

## 通过搜索引擎来实现 
搜索引擎会将所有需要搜索的数据使用算法做一个索引，以后在搜索的时候只要依据这个索引就可以找到相应的数据，搜索引擎建立索引的时候比较慢，但是索引一旦建立好了，那么以后在搜索数据的时候就会很快了

### django-hystack
这个插件是专门用来给django提供搜索的，django-hystack提供了一个搜索接口，底层可以依据自己的需求更换搜索引擎，它其实类似与django的ORM插件，提供了一个操作数据库的接口，底层具体使用哪个数据库是可以自己设置的。安装方式非常简单`pip install django-hystack`就可以了。

### 搜索引擎 

hystack支持的搜索引擎有Solr，Elasticsearch，Whoosh，Xapian等。Whoosh是基于纯Python实现的搜索引擎，检索速度快，集成方便，推荐使用Whoosh来使用。安装的话使用命令`pip install whoosh`就可以了。

### 继承步骤：
1. 在项目中安装`django-hystack`，在setting中将`hystack`放入INSTALLED_APPS中。
```python
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'haystack',  
]
```
2. 设置搜索引擎
```python
HAYSTACK_CONNECTIONS = {
    'default': {
        # 配置搜索引擎
        'ENGINE': 'DjangoBlog.whoosh_cn_backend.WhooshEngine',
        # 配置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
```
3. 创建索引类 
在需要搜索的app下面新建一个`search_indexes.py`的文件，名字必须是`search_indexes`,然后在里面创建索引类，示例代码：
```python 
from haystack import indexes
from django.conf import settings
from blog.models import Article, Category, Tag

# 新建索引类必须继承indexes.SearchIndex, indexes.Indexable这两个父类
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引主要字段
    text = indexes.CharField(document=True, use_template=True)

    # 获取模型 
    def get_model(self):
        return Article
    # 要索引的QuerySet对象
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='p').all() # 这里可以做过滤或者排序
```
4. 添加模版
在模版中定义需要索引的字段(也就是在标题中还是在内容中索引)
在temlplates文件夹中新建search文件夹，在search文件下新建indexes文件夹，在indexes下新建news(模型)文件夹 在news下新建`模型的名字小写_text.txt`文件,txt文件内容：
```
{{object.title}}
{{object.content}}
```
接着在templates文件夹下创建`search.html`模版文件，hystack会自动的在templates文件夹下寻找这个模版文件渲染，并且会给这个模版文件传入`page`,`paginator`,`query`等参数，其中`page` `paginator`分别是django内置的`page`类和`paginator`类的对象query是查询的关键字，我们通过`page.object_list`获取到查找出来的数据,示例代码如下：
```html
<ul class="news-list">
    {% for result in page.object_list% }
    {% with result.object as news %}
        {{ news.name }}
        {{news.publish_time }}
    {% endwith %}
    {% endfor%}
</ul>
```
5. url映射 
```python 
from django.urls import path,include
urlpatterns =[
    path("search/",include("hystack.urls"))
]
```
6. 创建索引使用命令`rebuild_index`,就是在manage.py的目录使用`python manage.py rebuild_index`,这是手动创建索引，还可以配置自动创建索引，在settings中加入下面的配置 
```python
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

7. 使用jieba分词替换Whoosh默认的分词
Whoosh默认是采用正则表达式来进行分词的，这对于英文来说足够了，但对于中文来说却支持不好，因此我们要替换为jieba分词。jieba分词是中文分词中最好用的免费的分词库，要使用jieba分词库，需要通过`pip install jieba`来安装。
安装成功后，拷贝文件whoosh_backend.py（该文件路径为python路径/lib/python2.7.5/site-packages/haystack/backends/whoosh_backend.py）拷贝到app下面，并重命名为whoosh_cn_backend.py，例如blog/whoosh_cn_backend.py。在文件导完包的代码下面添加下面的代码：
```python 
import jieba
from whoosh.analysis import Tokenizer, Token
class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        seglist = jieba.cut(value, cut_all=True)
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.startchar = start_char + value.find(w)
                t.endchar = start_char + value.find(w) + len(w)
            yield t
def ChineseAnalyzer():
    return ChineseTokenizer()
```
然后查找`analyzer=StemmingAnalyzer()`改为`analyzer=ChineseAnalyzer()`
然后在settings中更改自己定义的引擎
```
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'article.whoosh_cn_backend.WhooshEngine',      #article.whoosh_cn_backend便是你刚刚添加的文件
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'
    },
}
```
最后重新创建一下索引`python manage.py rebuild_index`就可以使用了。
### 语法高亮 
是通过一个模版标签来是实现的
在app的目录下新建2个py文件，`app01\templatetags\my_filters_and_tags.py`
`app01/templatetags/highlighting.py`

`app01\templatetags\my_filters_and_tags.py`代码：
```python
from __future__ import absolute_import, division, print_function, unicode_literals

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six

from haystack.utils import importlib

register = template.Library()


class HighlightNode(template.Node):
    def __init__(self, text_block, query, html_tag=None, css_class=None, max_length=None, start_head=None):
        self.text_block = template.Variable(text_block)
        self.query = template.Variable(query)
        self.html_tag = html_tag
        self.css_class = css_class
        self.max_length = max_length
        self.start_head = start_head

        if html_tag is not None:
            self.html_tag = template.Variable(html_tag)

        if css_class is not None:
            self.css_class = template.Variable(css_class)

        if max_length is not None:
            self.max_length = template.Variable(max_length)

        if start_head is not None:
            self.start_head = template.Variable(start_head)

    def render(self, context):
        text_block = self.text_block.resolve(context)
        query = self.query.resolve(context)
        kwargs = {}

        if self.html_tag is not None:
            kwargs['html_tag'] = self.html_tag.resolve(context)

        if self.css_class is not None:
            kwargs['css_class'] = self.css_class.resolve(context)

        if self.max_length is not None:
            kwargs['max_length'] = self.max_length.resolve(context)

        if self.start_head is not None:
            kwargs['start_head'] = self.start_head.resolve(context)

        # Handle a user-defined highlighting function.
        if hasattr(settings, 'HAYSTACK_CUSTOM_HIGHLIGHTER') and settings.HAYSTACK_CUSTOM_HIGHLIGHTER:
            # Do the import dance.
            try:
                path_bits = settings.HAYSTACK_CUSTOM_HIGHLIGHTER.split('.')
                highlighter_path, highlighter_classname = '.'.join(path_bits[:-1]), path_bits[-1]
                highlighter_module = importlib.import_module(highlighter_path)
                highlighter_class = getattr(highlighter_module, highlighter_classname)
            except (ImportError, AttributeError) as e:
                raise ImproperlyConfigured(
                    "The highlighter '%s' could not be imported: %s" % (settings.HAYSTACK_CUSTOM_HIGHLIGHTER, e))
        else:
            from .highlighting import Highlighter
            highlighter_class = Highlighter

        highlighter = highlighter_class(query, **kwargs)
        highlighted_text = highlighter.highlight(text_block)
        return highlighted_text


@register.tag
def myhighlight(parser, token):
    """
    Takes a block of text and highlights words from a provided query within that
    block of text. Optionally accepts arguments to provide the HTML tag to wrap
    highlighted word in, a CSS class to use with the tag and a maximum length of
    the blurb in characters.
    Syntax::
        {% highlight <text_block> with <query> [css_class "class_name"] [html_tag "span"] [max_length 200] %}
    Example::
        # Highlight summary with default behavior.
        {% highlight result.summary with request.query %}
        # Highlight summary but wrap highlighted words with a div and the
        # following CSS class.
        {% highlight result.summary with request.query html_tag "div" css_class "highlight_me_please" %}
        # Highlight summary but only show 40 characters.
        {% highlight result.summary with request.query max_length 40 %}
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if not len(bits) % 2 == 0:
        raise template.TemplateSyntaxError(u"'%s' tag requires valid pairings arguments." % tag_name)

    text_block = bits[1]

    if len(bits) < 4:
        raise template.TemplateSyntaxError(u"'%s' tag requires an object and a query provided by 'with'." % tag_name)

    if bits[2] != 'with':
        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'with'." % tag_name)

    query = bits[3]

    arg_bits = iter(bits[4:])
    kwargs = {}

    for bit in arg_bits:
        if bit == 'css_class':
            kwargs['css_class'] = six.next(arg_bits)

        if bit == 'html_tag':
            kwargs['html_tag'] = six.next(arg_bits)

        if bit == 'max_length':
            kwargs['max_length'] = six.next(arg_bits)

        if bit == 'start_head':
            kwargs['start_head'] = six.next(arg_bits)

    return HighlightNode(text_block, query, **kwargs)
```
`app01/templatetags/highlighting.py` 代码：
```python
# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.utils.html import strip_tags


class Highlighter(object):
    # 默认值
    css_class = 'highlighted'
    html_tag = 'span'
    max_length = 200
    start_head = False
    text_block = ''

    def __init__(self, query, **kwargs):
        self.query = query

        if 'max_length' in kwargs:
            self.max_length = int(kwargs['max_length'])

        if 'html_tag' in kwargs:
            self.html_tag = kwargs['html_tag']

        if 'css_class' in kwargs:
            self.css_class = kwargs['css_class']

        if 'start_head' in kwargs:
            self.start_head = kwargs['start_head']

        self.query_words = set([word.lower() for word in self.query.split() if not word.startswith('-')])

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        return self.render_html(highlight_locations, start_offset, end_offset)

    def find_highlightable_words(self):
        # Use a set so we only do this once per unique word.
        word_positions = {}

        # Pre-compute the length.
        end_offset = len(self.text_block)
        lower_text_block = self.text_block.lower()

        for word in self.query_words:
            if not word in word_positions:
                word_positions[word] = []

            start_offset = 0

            while start_offset < end_offset:
                next_offset = lower_text_block.find(word, start_offset, end_offset)

                # If we get a -1 out of find, it wasn't found. Bomb out and
                # start the next word.
                if next_offset == -1:
                    break

                word_positions[word].append(next_offset)
                start_offset = next_offset + len(word)

        return word_positions

    def find_window(self, highlight_locations):
        best_start = 0
        best_end = self.max_length

        # First, make sure we have words.
        if not len(highlight_locations):
            return (best_start, best_end)

        words_found = []

        # Next, make sure we found any words at all.
        for word, offset_list in highlight_locations.items():
            if len(offset_list):
                # Add all of the locations to the list.
                words_found.extend(offset_list)

        if not len(words_found):
            return (best_start, best_end)

        if len(words_found) == 1:
            return (words_found[0], words_found[0] + self.max_length)

        # Sort the list so it's in ascending order.
        words_found = sorted(words_found)

        # We now have a denormalized list of all positions were a word was
        # found. We'll iterate through and find the densest window we can by
        # counting the number of found offsets (-1 to fit in the window).
        highest_density = 0

        if words_found[:-1][0] > self.max_length:
            best_start = words_found[:-1][0]
            best_end = best_start + self.max_length

        for count, start in enumerate(words_found[:-1]):
            current_density = 1

            for end in words_found[count + 1:]:
                if end - start < self.max_length:
                    current_density += 1
                else:
                    current_density = 0

                # Only replace if we have a bigger (not equal density) so we
                # give deference to windows earlier in the document.
                if current_density > highest_density:
                    best_start = start
                    best_end = start + self.max_length
                    highest_density = current_density

        return (best_start, best_end)

    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # Start by chopping the block down to the proper window.
        # text_block为内容，start_offset,end_offset分别为第一个匹配query开始和按长度截断位置
        text = self.text_block[start_offset:end_offset]

        # Invert highlight_locations to a location -> term list
        term_list = []

        for term, locations in highlight_locations.items():
            term_list += [(loc - start_offset, term) for loc in locations]

        loc_to_term = sorted(term_list)

        # Prepare the highlight template
        if self.css_class:
            hl_start = '<%s class="%s">' % (self.html_tag, self.css_class)
        else:
            hl_start = '<%s>' % (self.html_tag)

        hl_end = '</%s>' % self.html_tag

        # Copy the part from the start of the string to the first match,
        # and there replace the match with a highlighted version.
        # matched_so_far最终求得为text中最后一个匹配query的结尾
        highlighted_chunk = ""
        matched_so_far = 0
        prev = 0
        prev_str = ""

        for cur, cur_str in loc_to_term:
            # This can be in a different case than cur_str
            actual_term = text[cur:cur + len(cur_str)]

            # Handle incorrect highlight_locations by first checking for the term
            if actual_term.lower() == cur_str:
                if cur < prev + len(prev_str):
                    continue

                # 分别添上每个query+其后面的一部分（下一个query的前一个位置）
                highlighted_chunk += text[prev + len(prev_str):cur] + hl_start + actual_term + hl_end
                prev = cur
                prev_str = cur_str

                # Keep track of how far we've copied so far, for the last step
                matched_so_far = cur + len(actual_term)

        # Don't forget the chunk after the last term
        # 加上最后一个匹配的query后面的部分
        highlighted_chunk += text[matched_so_far:]

        # 如果不要开头not start_head才加点
        if start_offset > 0 and not self.start_head:
            highlighted_chunk = '...%s' % highlighted_chunk

        if end_offset < len(self.text_block):
            highlighted_chunk = '%s...' % highlighted_chunk

        # 可见到目前为止还不包含start_offset前面的，即第一个匹配的前面的部分（text_block[:start_offset]），如需展示(当start_head为True时)便加上
        if self.start_head:
            highlighted_chunk = self.text_block[:start_offset] + highlighted_chunk
        return highlighted_chunk
```
在使用之前需要配置haystack_connections
```
HAYSTACK_CONNECTIONS = {
    'default': {
        # 配置搜索引擎
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 配置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
```
然后就可以在模版中使用了
```html
{% load my_filters_and_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
// 标签使用
{% myhighlight "112" with "112" %}
// haystack传递过来的数据放在 page.object_list里面 
// 遍历page.object_list 得到一个result对象
// result.object才是模型对象
// query 是查询的关键字
{% myhighlight page.object_list.0.object.name with query %}
// <--高亮样式-->
<style>
    span.highlighted {
        color: red;
        font-weight: 700;
    }
</style>

</body>
</html>
```