# markdown的语法规则

## 什么是markdown？
`markdown`是一种轻量级标记语言，它允许人们使用易读易写的纯文本格式编写文档。就连文字排版、画图、等等都像打字一样输入即可自动生成，非常高效。
目前有很多主流文本应用都支持markdown编辑，比如：`GitHub`，简书，印象笔记，`sourceforge`等等。下面示例语法都用印象笔记为例。


## markdown编辑文本

编辑文本是我们写文档最常用的功能，而编辑文本中，打字什么的所有软件都是一样的，没有多大区别。效率区别最大的就是文档样式排版。下面我们就看看`markdown`语言，如何像打字一样排版。

1. 标题
要写标题，用markdown标记，只需要一个# 后面加上文字即可。
```markdown
# 一级标题
## 二级标题
### 三级标题
```
以此类推，多少个#号，就是多少级标题。是不是非常的简单。
注意：不同的软件支持可能会有细微差别，有的需要在#号后加空格。

2. 文字格式

我们编辑文档最常用到的文字处理就是：加粗、斜体、粗体加斜体，下划线，删除线等等，现在我们来看看用markdown如何简单编辑。

**这是加粗字体**，

*这是斜体*，

***这是粗体加斜体***
~~这是带删除线~~
分割线输入---即可
文档缩进，按tab键即可，换行按回车即可。

3. 引用内容 
    - 文字引用
        我们写文档，有时候需要引用外部文字。要表示文字是引用的，只需要加上>即可。
        ```
        >一级引用内容

        >>二级引用内容

        >>>三级引用内容
        ```
        如果需要为文字添加链接，只需要将文字用[ ]框起来，并跟在在后面输入URL，用（）括起来。
        语法示例：
        [百度](baidu.com)

    - 图片引用

        引用网络图片，只需要输入图片URL即可。
        语法示例：
        `![image](URL)`

    - 代码引用
        如果需要引用代码块，则需要将代码段落用 ``` ```符号括起来。
        语法示例：
        ```python
        代码块
        ```
4. 列表项
    列表项仅仅需要和我们日常习惯一样，输入*号，1.符号，等标记符号即可。
    *号代表实心圆点，通常是无序列表。1.就是带数字的有序列表

## 表格

类似于插入excel表格。
语法示例：
| 月份 |潜在机会 |立项阶段 |方案阶段 |招投标阶段 |签单成交 |
| --- | --- | --- | --- | --- | --- |
| 1月 | 520 | 100 |56 |25 | 18 |
| 2月 | 480 | 82 | 30 | 8 | 5 |
| 3月 | 550 | 95 | 48 | 12 |12 |

结果如下
![表格](http://qqpublic.qpic.cn/qq_public/0/0-2956721014-0D77965D239EC83E3375A6E1C899B87F/0?fmt=jpg&h=270&ppv=1&size=12&w=497)
## 图表

语法示例：
```chart
月份,预算,签单,毛利,净利
6月,50000,48000,20000,10000
7月,30000,21000,14000,8000
8月,50000,47000,26000,23000
9月,70000,62000,33000,21000
10月,60000,55000,34000,20000
11月,40000,35000,19000,16000
type: line
title: 月度业绩表
x.title: 月份
y.title: 金额
y.suffix: ￥
```
![结果](http://qqpublic.qpic.cn/qq_public/0/0-2263462150-BCA18B72D9252CA91CD52BDE5D59A5D2/600?fmt=jpg&h=223&ppv=1&size=12&w=600)