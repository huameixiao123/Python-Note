# html笔记

# 基础知识

## 认识html
HTML 不是一种编程语言，而是一种标记语言 (markup language)，是网页制作所必备的。用于按不同标签声明网页中的内容。

## 文件命名

1. 使用小写字线命名文件，不要出现中文字符
2. 扩展名标准是.html，当然也可以使用.htm
3. 多个单词可以使用- 或 _ 连接，建议使用- 字符如user-create.html

## URL

统一资源定位符，用于表示资源在网络上的地址，每个部分以/进行分隔。

`https://www.houdunren.com/edu/front/lesson/298.html`
参数 | 说明
-|-
https |  访问协议 http或https、ftp、mailto
www.houdunren.com  | 服务器地址
edu/front/lesson   | 资源目录
298.html    |文件名

## 访问路径

1. 绝对路径
绝对路径包含主机+服务器地址+目录+文件名的完整路径
`https://www.houdunren.com/edu/front/lesson/298.html`
2. 相对路径
相对路径是指相对当前目录的地址
```html
# 当前目录的文件
2.html

# 上级目录中的文件
../3.html

# 子目录中的文件
block/user.html

# 根目录中的文件
/bootstrap.html
```

## 注释

使用注释对一段html代码进行说明，方便自己或同事在未来清楚的明白代码意图。
```html
<!-- 这是导航条 START -->
<header role="navigation">
  <nav>
    <ul>
      <li>
        <a href="">后盾人首页</a>
      </li>
      <li>
        <a href="">系统课程</a>
      </li>
    </ul>
  </nav>
</header>
<!-- 这是导航条 END -->
```

# 页面结构

## 语义标签

`HTML`标签都有具体语义，非然技术上可以使用`div`标签表示大部分内容，但选择清晰的语义标签更容易让人看明白。比如 `h1`表示标题、`p`标签表示内容、强调内容使用`em`标签。

```html
<article>
    <h1>后盾人</h1>
    <p>在线学习平台</p>
</article>
```

## 嵌套关系

元素可以互相嵌套包裹，即元素存在父子级关系。

```html
<article>
  <h1>后盾人</h1>
  <div>
    <p>在线学习平台</p>
    <span>houdunren.com</span>
  </div>
</article>
```
![嵌套](http://houdunren.gitee.io/note/assets/img/image-20190725120421647.95e6e1d0.png)

## 基本结构
下面是HTML文档的基本组成部分

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="keyword" content="Mysql,Laravel,Javascript,HTML,CSS,ES6,TYPESCRIPT,后盾人,后盾人教程" />
    <meta name="description" content="后盾人专注WEB开发，高密度更新视频教程" />
    <title>后盾人</title>
</head>
<body>
   
</body>
</html>
```
标签 | 说明
-|-
DOCTYPE| 声明为HTML文档
html   | lang:网页的语言，如en/zh等，非必选项目
head  |  文档说明部分，对搜索引擎提供信息或加载CSS、JS等
title |  网页标题
keyword| 搜索引擎说明你的网页的关键词
description| 向搜索引擎描述网页内容的摘要信息
body  |  页面主体内容

## 内容标题

标题使用 h1 ~ h6 来定义，用于突出显示文档内容。

1. 从 h1到h6对搜索引擎来说权重会越来越小
2. 页面中最好只有一个h1标签
3. 标题最好不要嵌套如 h1内部包含 h2
下面是使用默认样式的标题效果，掌握CSS后我们就可以随意美化了。
```html
<h1>后盾人</h1>
<h2>houdunren.com</h2>
<h3>hdcms.com</h3>
<h4>houdunwang.com</h4>
<h5>doc.houdunren.com</h5>
<h6>www.hdcms.com</h6>
```
![内容标题](http://houdunren.gitee.io/note/assets/img/image-20190725143133097.6b8ac92e.png)

## 页眉页脚

`header`
`header`标签用于定义文档的页眉，下图中的红色区域都可以使用header标签构建。

![header](http://houdunren.gitee.io/note/assets/img/image-20190725143914516.bcffc293.png)
```html
<body>
    <header>
        <nav>
            <ul>
                <li><a href="">系统学习</a></li>
                <li><a href="">视频库</a></li>
            </ul>
        </nav>
    </header>
    <article>
        <h2>后盾人网站动态</h2>
        <ul>
            <li><a href="">完成签到 开心每一天</a></li>
            <li><a href="">完成签到 来了，老铁</a></li>
        </ul>
    </article>
    ...
</body>
```

`footer`
`footer` 标签定义文档或节的页脚，页脚通常包含文档的作者、版权信息、使用条款链接、联系信息等等。
![footer](http://houdunren.gitee.io/note/assets/img/image-20190725144209867.e3ad5cf8.png)

```html
<body>
    ...
    <article>
        <h2>后盾人网站动态</h2>
        <ul>
            <li><a href="">完成签到 开心每一天</a></li>
            <li><a href="">完成签到 来了，老铁</a></li>
        </ul>
    </article>
    <footer>
        <p>
            我们的使命：传播互联网前沿技术，帮助更多的人实现梦想
        </p>
    </footer>
</body>
```

## 导航元素

在`HTML`中使用`nav`设置导航链接。

![](http://houdunren.gitee.io/note/assets/img/image-20190725155313952.6de67df5.png)

```html
<header>
        <nav>
            <ul>
                <li>
                    <a href="">系统学习</a>
                </li>
                <li>
                    <a href="">视频库</a>
                </li>
            </ul>
        </nav>
</header>
```

## 主要区域

`HTML5`中使用 `main` 标签表示页面主要区域，一个页面中`main`元素最好只出现一次。
![](http://houdunren.gitee.io/note/assets/img/image-20190725160319383.782b883c.png)

```html
<body>
        ...
    <main>
        <article>
            <h2>网站动态</h2>
            <ul>
                <li><a href="">完成签到 开心每一天</a></li>
                <li><a href="">完成签到 来了，老铁</a></li>
            </ul>
        </article>
    </main>
    ...
</body>
```

## 内容区域

使用 `article` 标签规定独立的自包含内容区域。不要被单词的表面意义所局限，`article` 标签表示一个独立的内容容器。

![](http://houdunren.gitee.io/note/assets/img/image-20190725161743627.feb72e82.png)

```html
<main>
    <article>
    <h2>后盾人网站动态</h2>
    <ul>
      <li><a href="">完成签到 开心每一天</a></li>
      <li><a href="">完成签到 来了，老铁</a></li>
    </ul>
    </article>
</main>
```

## 区块定义

使用 `section` 定义一个区块，一般是一组相似内容的排列组合。

![](http://houdunren.gitee.io/note/assets/img/image-20190725162232253.578dfcf0.png)

```html
<main>
   <article>
     <section>
       <h2>锁机制</h2>
     </section>
     <section>
      <h2>事物处理</h2>
     </section>
   </article>
</main>
```

## 附加区域

使用 `aside` 用于设置与主要区域无关的内容，比如侧面栏的广告等。

![](http://houdunren.gitee.io/note/assets/img/image-20190725164542103.82f1400c.png)

```html
<body>
  <main>
    <article>
      ...
    </article>
    </main>
    <aside>
      <h2>社区小贴</h2>
      <p>后盾人是一个主张友好、分享、自由的技术交流社区。</p>
    </aside>
  </main>
</body>
```

## 通用容器

`div` 通用容器标签是较早出现的，也是被大多数程序员使用最多的容器。不过我们应该更倾向于使用有语义的标签如`article/section/aside/nav` 等。

有些区域这些有语义的容器不好表达，这时可以采用`div`容器，比如轮播图效果中的内容。

![](http://houdunren.gitee.io/note/assets/img/image-20190725165638145.edf4b8f0.png)

```html
<div>
  <header>
    <nav>
      <ul>
        <li><a href="">后盾人</a></li>
        <li><a href="">系统课程</a></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <article>
      <section>
        <h2>事物处理</h2>
      </section>
    </article>
    <aside>
      <h2>社区小贴</h2>
      <p>后盾人是一个主张友好、分享、自由的技术交流社区。</p>
    </aside>
  </main>
  
  <footer>
    <p>
    我们的使命：传播互联网前沿技术，帮助更多的人实现梦想
    </p>
  </footer>
</div>
```

# 标签
标签| 作用
p | p标签标记了一个段落内容。
pre| 原样显示文本内容包括空白、换行等。
br | 在html 中回车是忽略的，使用 br 标签可以实现换行效果。
span | span 标签与 div 标签都是没有语义的，span 常用于对某些文本特殊控制，但该文本又没有适合的语义标签。
small |  用于设置描述、声明等文本。
time | 标签定义日期或时间，或者两者。
abbr　| abbr标签用于描述一个缩写内容
sub | 用于数字的下标内容
sup | 用于数字的上标内容
del | del 标签表示删除的内容，ins 一般与 del 标签配合使用描述更新与修正。
s | s 标签显示效果与 del 相似，但语义用来定义那些不正确、不准确或没有用的文本。
code | 用于显示代码块内容，一般需要代码格式化插件完成。
progress | 用于表示完成任务的进度，当游览器不支持时显示内容。
strong | strong 标签和 em 一样，用于强调文本，但是它们的强调程度不同。
mark | 用于突出显示文本内容，类似我们生活中使用的马克笔。
cite | cite 标签通常表示它所包含的文本对某个参考文献的引用，或文章作者的名子。
blockquote | blockquote 用来定义摘自另一个源的块引用
q | q 用于表示行内引用文本，在大部分浏览器中会加上引号。
address | 用于设置联系地址等信息，一般将address 放在footer 标签中。

# 图片处理

## 图像格式

1. 网络带宽成本很高，图片处理在保证用户体验好的前端下，文件尺寸也要尽可能小
2. 图片属性静态文件，不要放在`WEB`服务器上，而放在云储存服务器上并使用`CDN`加速
3. 以`JPEG`类型优先使用，文件尺寸更小
4. 小图片使用`PNG`，清晰度更高，因为文件尺寸小，文件也不会太大
5. 网页图标建议使用`css`字体构建如 `iconfont` 或 `fontawesome`

格式  |说明 | 透明
-|-| -
PNG |无损压缩格式，适合图标、验证码等。有些小图标建议使用css字体构建。  |支持
GIF |256色，可以产生动画效果（即GIF动图）   |支持
JPEG |   有损压缩的类型，如商品、文章的图片展示 |

下图的网站标志使用png 类型，这样图片清晰，同时有透明色，当页面底色改变时也不需要修改图片。
![](http://houdunren.gitee.io/note/assets/img/image-20190727162631092.0328dd30.png)

## 保存透明图
下面介绍在PhotoShop 中快速生成透明 png 的图片效果。
1. 保证没有纯色的底
![](http://houdunren.gitee.io/note/assets/img/image-20190727163814195.bd0ba8cd.png)
2. 选择导出为png格式即可
![](http://houdunren.gitee.io/note/assets/img/image-20190727163912804.2e747827.png)

## 使用图片

在网页中使用 `img` 标签展示图片，图片的大小、边框、倒角效果使用`css`处理。
`<img src="houdunren.png" alt="后盾人"/>`
属性 | 说明
-|-
src| 图片地址
alt| 图像打开异常时的替代文本

# 网页链接

不能能过一个页面展示网站的所有功能，需要在不同页面中跳转，这就是链接所起到的功能。

`<a href="http://doc.houdunren.com" target="_blank" title="文档库">后盾人文档库</a>`

选项  |说明
-|-
href   | 跳转地址
target | _blank 新窗口打开 _self 当前窗口打开
title  | 链接提示文本

## 打开窗口

下面设置 target 属性在指定窗口打开。
```html
<a href="https://www.houdunren.com" target="hdcms">
        在IFRAME中打开
</a>
<script>
    window.open('https://www.hdcms.com', 'hdcms');
</script>
```

## 锚点链接

锚点可以设置跳转到页面中的某个部分。

1. 为元素添加`id` 属性来设置锚点
2. 设置 `a` 标签的 `href`属性
3. html
```html
<a href="#comment-1">跳转到评论区</a>
<div style="height: 1000px;"></div>

<div id="comment-1" style="background: green;">
    这是后盾人评论内容区
</div>
```
4. 也可以跳转到不同页面的锚点
```html
<a href="article.html#comment-1">跳转到评论区</a>
```
## 邮箱链接

除了页面跳转外可以指定其他链接。使用以下方式也有缺点，邮箱可能会被恶意用户采集到，所以有些用户使用 `houdunren#qq.com` 然后提示用户 `请将#改为@后发邮件`的提示形式。
```<a href="mailto:2300071698@qq.com">给后盾人发送邮件</a>
```

## 拨打电话
点击以下链接后，手机会询问用户是否拨打电话。

`<a href="tel:99999999999">联系客服</a>`

## 下载文件
默认情况下使用链接可以下载浏览器无法处理的文件，如果下载图片需要后台语言告之浏览器mime类型（可查看后盾人PHP）相关课程。
`<a href="https://www.hdcms.com/HDCMS-201905072207.zip">下载HDCMS</a>`

# 表单

表单是服务器收集用户数据的方式。

## FORM

一般情况下表单项要放在 FORM 内提交。

```html 
<form action="hd.php" method="POST">
    <fieldset>
        <legend>测试</legend>
        <input type="text">
    </fieldset>
</form>
```
属性 | 说明
-|-
action | 后台地址
method | 提交方式 GET 或 POST

## LABEL

使用 label 用于描述表单标题，当点击标题后文本框会获得焦点，需要保证使用的ID在页面中是唯一的。
```html 
<form action="hd.php" method="POST" novalidate>
<label for="title">标题</label>
<input type="text" name="title" id="title">
</form>
```
也可以将文本框放在 label 标签内部，这样就不需要设置 id 与 for 属性了

## INPUT

文本框用于输入单行文本使用，下面是常用属性与示例。
属性  |说明
-|-
type |   表单类型默认为 text
name  |  后台接收字段名
required  |  必须输入
placeholder |提示文本内容
value   |默认值
maxlength   |允许最大输入字符数
size   | 表单显示长度，一般用不使用而用 css 控制
disabled   | 禁止使用，不可以提交到后台
readonly   | 只读，可提交到后台

```html 
<form action="hd.php" method="POST" novalidate>
        <fieldset>
            <legend>文本框</legend>
            <input type="text" name="title" required placeholder="请输入标题" maxlength="5" value="" size="100">
        </fieldset>
</form>
```

## 其他类型
通过设置表单的 type 字段可以指定不同的输入内容。

类型 | 说明
-|-
email |  输入内容为邮箱
url| 输入内容为URL地址
password   | 输入内容为密码项
tel| 电话号，移动端会调出数字键盘
search  |搜索框
hidden | 隐藏表单
submit | 提交表单

## HIDDEN

隐藏表单用于提交后台数据，但在前台内容不显示也以在其上做用样式表也没有意义。
`<input type="hidden" name="id" value="1">`

## 提交表单

创建提交按钮可以将表单数据提交到后台，有多种方式可以提交数据如使用AJAX，或HTML的表单按钮。

1. 使用input构建提交按钮，如果设置了name值按钮数据也会提交到后台，如果有多个表单项可以通过些判断是哪个表单提交的。
`<input type="submit" name="submit" value="提交表单">`
2. 使用button也可以提交，设置type属性为submit 或不设置都可以提交表单。
`<button type="submit">提交表单</button>`

## 禁用表单
通过为表单设置 `disabled` 或 `readonly` 都可以禁止修改表单，但 `readonly`表单的数据可以提交到后台。
`<input type="text" name="web" value="houdunren.com" readonly>`

## PATTERN

表单可以通过设置 `pattern` 属性指定正则验证，也可以使用各种前端验证库如 `formvalidator` 或 `validator.js`。

属性 | 说明
-|-
pattern |正则表达式验证规则
oninvalid   |输入错误时触发的事件

```html
<form action="">
    <input type="text" name="username" pattern="[A-z]{5,20}" 
    oninvalid="validate('请输入5~20位字母的用户名')">
    <button>提交</button>
</form>
    
<script>
    function validate(message) {
        alert(message);
    }
</script>
```

## TEXTAREA
文本域指可以输入多行文本的表单，当然更复杂的情况可以使用编辑器如`ueditor`、`ckeditor`等。

选项 | 说明
-|-
cols   | 列字符数（一般使用css控制更好）
rows  |  行数（一般使用css控制更好）

`<textarea name="content" cols="30" rows="3">houdunren.com</textarea>`

## SELECT
下拉列表项可用于多个值中的选择。

选项 | 说明
-|-
multiple  |  支持多选
size   | 列表框高度
optgroup  |  选项组
selected  |  选中状态
option|  选项值

```html
<select name="lesson">
        <option value="">== 选择课程 ==</option>
        <optgroup label="后台">
            <option value="php">PHP</option>
            <option value="linux">LINUX</option>
            <option value="mysql">MYSQL</option>
        </optgroup>
        <optgroup label="前台">
            <option value="php">HTML</option>
            <option value="linux">JAVASCRIPT</option>
            <option value="mysql">CSS</option>
        </optgroup>
</select>
```

## RADIO

单选框指只能选择一个选项的表单，如性别的选择男、女、保密 只能选择一个
选项 |  说明
-|-
checked | 选中状态

```html
<input type="radio" name="sex" value="boy" id="boy">
<label for="boy">男</label>

<input type="radio" name="sex" value="girl" id="girl" checked>
<label for="girl">女</label>
```

## CHECKBOX
复选框指允许选择多个值的表单。
```html
<fieldset>
        <legend>复选框</legend>
        <input type="checkbox" name="sex" value="boy" id="boy">
        <label for="boy">PHP</label>

        <input type="checkbox" name="sex" value="girl" id="girl" checked>
        <label for="girl">MYSQL</label>
</fieldset>
```

## 文件上传

文件上传有多种方式，可以使用插件或JS拖放上传处理。HTML本身也提供了默认上传的功能，只是上传效果并不是很美观。

选项|  说明
-|-
multiple  |  支持多选
accept | 允许上传类型 .png,.psd 或 image/png,image/gif

```html
<form action="" method="POST" enctype="multipart/form-data">
    <fieldset>
        <input type="file" name="icon" multiple="multiple" accept="image/png,image/gif">
    </fieldset>
    <button>保存</button>
</form>
```
## 日期与时间

属性 |  说明
-|-
step  |   间隔：date 缺省是1天，week缺省是1周，month缺省是1月
min|  最小时间
max | 最大时间
1. 日期选择
`<input type="date" step="5" min="2020-09-22" max="2025-01-15" name="datetime"`
2. 周选择
`<input type="week">`
3. 月选择
`<input type="month">`
4. 日期与时间
`<input type="datetime-local" name="datetime">`

## DATELIST

input表单的输入值选项列表
```html
<form action="" method="post">
  <input type="text" list="lesson">
  <datalist id="lesson">
    <option value="PHP">后台管理语言</option>
    <option value="CSS">美化网站页面</option>
    <option value="MYSQL">掌握数据库使用</option>
  </datalist>
</form>
```
## autocomplete

浏览器基于之前键入过的值，应该显示出在字段中填写的选项。
```html
<form action="">
  <input type="search" autocomplete="on" name="content" />
  <button>提交</button>
</form>
```

## 列表
列表的使用与word 等软件的列表概念相似，只不过是应用在网页展示中。

1. 有序列表
有序列表是指有数字编号的列表项，可以使用CSS定义更多样式，具体请查看CSS章节。

```html
<style>
        .li-style1{
            /* 
            circle      空心圆
            disc        实心圆
            square      实心方块
            decimal     数字
            upper-alpha 大写字母
            lower-alpha 小写字母
            upper-roman 大写罗马数字
            lower-roman 小写罗马数字
             */
            list-style-type: decimal;
        }
        
        .li-style2{
            /* 取消风格 */
            list-style: none;
        }
        .li-style3{
            /*inside 内部 outside 外部（默认）*/
            list-style-position: inside;
        }
</style>

<ol start="1">
    <li>后盾人</li>
    <li>houdunren.com</li>
    <li>hdcms.com</li>
</ol>
```
2. 无序列表
没有数字编号的列表项，可以使用CSS定义更多样式，具体请查看CSS章节。
```html
<ul>
    <li>后盾人</li>
    <li>houdunren.com</li>
    <li>hdcms.com</li>
</ul>
```

3. 描述列表
描述列表指每个列表项有单独的标题。

```html
<dl>
    <dt>开源产品</dt>
    <dd>hdcms内容管理系统</dd>
    <dd>hdjs前库组件库</dd>
    
    <dt>网站导航</dt>
    <dd>houdunren.com</dd>
    <dd>houdunwang.com</dd>
</dl>
```

# 表格

表格在网页开发中使用频率非常高，尤其是数据展示时。

## 基本使用

属性  说明
-|-
caption 表格标题
thead   表头部分
tbody   表格主体部分
tfoot   表格尾部

```html
<table border="1">
        <caption>后盾人表格标题</caption>
        <thead>
            <tr>
                <th>标题</th>
                <th>时间</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>后盾人</td>
                <td>2020-2-22</td>
            </tr>
        </tbody>
</table>
```

## 单元格合并

下面是水平单元格合并

```html
<table border="1">
        <thead>
            <tr>
                <th>标题</th>
                <th>时间</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td colspan="2">后盾人 2020-2-22</td>
            </tr>
        </tbody>
    </table>
```

## 下面是垂直单元格合并
```html
<table border="1">
        <thead>
            <tr>
                <th>标题</th>
                <th>时间</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td rowspan="2">后盾人</td>
                <td>2030-03-19</td>
            </tr>
            <tr>
                <td>2035-11-08</td>
            </tr>
        </tbody>
</table>
```

## 视频

Adobe与苹果公司对 `FLASH`都不支持或消极状态，这时HTML提供对视频格式的支持，除了使用`html`提供的标签来播放视频外，也有很多免费或付费的插件，如`video.js` 、阿里云播放器 等等。

属性说明

属性 | 描述
-|-
autoplay  |  如果出现该属性，则视频在就绪后马上播放（需要指定类型如 type="video/mp4")。
preload| 如果出现该属性，则视频在页面加载时进行加载，并预备播放。如果使用 "autoplay"，则忽略该属性。
如果视频观看度低可以设置为 preload="none" 不加载视频数据减少带宽。
如果设置为 preload=metadata值将加载视频尺寸或关键针数据，目的也是减少带宽占用。
设置为preload="auto" 时表示将自动加载视频数据
controls  |  如果出现该属性，则向用户显示控件，比如播放按钮。
height | 设置视频播放器的高度。
width |  设置视频播放器的宽度。
loop  |  如果出现该属性，则当媒介文件完成播放后再次开始播放。
muted | 规定视频的音频输出应该被静音。
poster | 规定视频下载时显示的图像，或者在用户点击播放按钮前显示的图像。
src |要播放的视频的 URL。
```html
<video src="houdunren.mp4" autoplay="autoplay" 
    loop muted controls width="800" height="200">
    
    <source src="houdunren.mp4" type="video/mp4">
  <source src="houdunren.webm" type="video/webm">
  
</video>
```

## 声音
HTML对声音格式文件也提供了很好的支持。

属性说明

属性 | 描述
-|-
autoplay  |  如果出现该属性，则视频在就绪后马上播放。
preload |如果出现该属性，则视频在页面加载时进行加载，并预备播放。如果使用 "autoplay"，则忽略该属性。
如果视频观看度低可以设置为 preload="none" 不加载视频数据减少带宽。
如果设置为 preload=metadata值将加载视频尺寸或关键针数据，目的也是减少带宽占用。
设置为preload="auto" 时表示将自动加载视频数据
controls |   如果出现该属性，则向用户显示控件，比如播放按钮。
loop  |  如果出现该属性，则当媒介文件完成播放后再次开始播放。
muted |  规定视频的音频输出应该被静音。
src|要播放的视频的 URL。

```html
<audio controls autoplay loop preload="auto">
    <source src="houdunren.ogg" type="audio/ogg">
    <source src="houdunren.mp3" type="audio/mp3">
</audio>
```