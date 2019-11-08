# Flask-Restful笔记：

### 安装：
Flask-Restful需要在Flask 0.8以上的版本，在Python2.6或者Python3.3上运行。通过pip install flask-restful即可安装。

### 基本使用：
1. 从`flask_restful`中导入`Api`，来创建一个`api`对象。
2. 写一个视图函数，让他继承自`Resource`，然后在这个里面，使用你想要的请求方式来定义相应的方法，比如你想要将这个视图只能采用`post`请求，那么就定义一个`post`方法。
3. 使用`api.add_resource`来添加视图与`url`。
示例代码如下：
```python
class LoginView(Resource):
    def post(self,username=None):
        return {"username":"zhiliao"}

api.add_resource(LoginView,'/login/<username>/','/regist/')
```
注意事项：
* 如果你想返回json数据，那么就使用flask_restful，如果你是想渲染模版，那么还是采用之前的方式，就是`app.route`的方式。
* url还是跟之前的一样，可以传递参数。也跟之前的不一样，可以指定多个url。
* endpoint是用来给url_for反转url的时候指定的。如果不写endpoint，那么将会使用视图的名字的小写来作为endpoint。


### 参数验证：
Flask-Restful插件提供了类似WTForms来验证提交的数据是否合法的包，叫做reqparse。以下是基本用法：
    ```python
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,help='请输入用户名')
    args = parser.parse_args()
    ```
add_argument可以指定这个字段的名字，这个字段的数据类型等。以下将对这个方法的一些参数做详细讲解：
1. default：默认值，如果这个参数没有值，那么将使用这个参数指定的值。
2. required：是否必须。默认为False，如果设置为True，那么这个参数就必须提交上来。 3. type：这个参数的数据类型，如果指定，那么将使用指定的数据类型来强制转换提交上来的值。
4. choices：选项。提交上来的值只有满足这个选项中的值才符合验证通过，否则验证不通过。
5. help：错误信息。如果验证失败后，将会使用这个参数指定的值作为错误信息。
6. trim：是否要去掉前后的空格。

其中的type，可以使用python自带的一些数据类型，也可以使用flask_restful.inputs下的一些特定的数据类型来强制转换。比如一些常用的：
1. url：会判断这个参数的值是否是一个url，如果不是，那么就会抛出异常。
2. regex：正则表达式。
3. date：将这个字符串转换为datetime.date数据类型。如果转换不成功，则会抛出一个异常。
