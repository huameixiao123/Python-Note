# VueRouter笔记

## 基本使用：
1. 创建一个`VueRouter`对象：`new VueRouter()`。
2. 在`VueRouter`中，需要传递一个`routes`参数。这个参数是一个数组类型，数组中存储的是对象，对象中最少要有两个属性，一个是`path`，代表`url`，第二个是`component`，代表数据更新的组件。示例代码如下：
  ```js
  let router = new VueRouter({
      routes: [
        {path: "/",component: index},
        {path: "/find",component: find},
        {path: "/friend",component: friend}
      ]
    })
  ```
3. 将`router`传给`Vue`。
4. 把网页中之前的`a`标签，替换成`router-link`。
5. 使用`router-view`指定网页中哪个地方要被更新。


## 动态路由：
1. 在url中，通过定义一个参数，那么以后url中就可以动态的传递这个参数。语法是：`/profile/:参数名`
2. 在组件中，可以通过`this.$route.params.参数名`拿到，或者是组件的模板中，可以通过`$route.params.参数名`拿到。
3. `this.$route`和`this.$router`的区别：
  * `this.$route`：代表的是当前这个路由里的一些信息集合。比如`params`，`query`，`fullPath`等。
  * `this.$router`：代表的是全局的`VueRouter`对象。

## 组件复用：
当使用路由参数时，例如从/user/foo导航到/user/bar，原来的组件实例会被复用。因为两个路由都渲染同个组件，比起销毁再创建，复用则显得更加高效。不过，这也意味着组件的生命周期钩子不会再被调用。
组件复用后，生命周期函数不会被重复调用，那么如果数据更新了，该怎么做相应的处理。有两种解决方案：
1. 监听`this.$route`属性。通过判断`to`和`from`来获取更新的数据。
2. 使用导航守卫的`beforeRouteUpdate`方法，也可以获取`to`和`from`，但是这个函数记得调用`next()`，否则页面不会进行更新。

## 404配置：
1. 前端的页面配置：在所有路由后面增加一个`*`的url，让这个url映射到一个404的组件。
2. 数据不存在的处理：这种情况，前端是没法判断存不存在的，只能通过访问服务器来判断存不存在。如果服务器返回不存在，那么我们可以通过`this.$router.replace`，跳转到404页面。

## 路由嵌套（子路由）：
1. 在大的路由下面，有时候想要使用一些子路由来切换数据。那么这时候可以使用路由嵌套。
2. 首先在定义路由的时候，不需要在`routes`中单独添加一个映射。而应该放在父路由的`children`中：
   ```js
   let router = new VueRouter({
      routes: [
        {
          path: "/",
          component: index
        },
        {
          path: "/user/:userid",
          component: user,
          children: [
            {path: "",component: setting},
            {path: "setting",component: setting},
            {path: "message",component: message}
          ]
        }
      ]
    })
   ```
3. 在父路由的组件中，要记得添加路由出口`<router-view>`。示例代码：
  ```js
    <div>
      <h1>我的主页</h1>
      <ul class="nav nav-tabs">
        <li role="presentation" class="active">
          <router-link to="/user/123/setting">设置</router-link>
        </li>
        <li role="presentation">
          <router-link to="/user/123/message">消息</router-link>
        </li>
      </ul>
      <router-view></router-view>
    </div>
  ```

## 编程式导航：
1. `this.$router.push`：转到下一个url，会把新转入的url添加到浏览器的history中。push的参数：
    * 字符串：直接就是路径。
    * 对象：path和name都可以。但是如果使用了path，那么参数就必须要放到path中，放到params中没有效果。
2. `this.$router.replace`：跟push是一样的，只不过是替换当前的页面。
3. `this.$router.go`：往前和往后。

## 路由名称：
可以在定义路由的时候指定name，使用的时候，可以直接传递name值就可以了。

## 命名视图（多组件）：
在一个页面中，可以通过命名视图展示多个组件。在实现的时候，有以下几个步骤：
1. 在定义路由的时候，需要传递`components`，然后把所有需要展示的路由都放到这个里面。`components`是一个对象，{name:组件}的映射。
2. 在模板中，就是通过`<router-view name="组件名"></router-view>`来实现。

## 重定向和别名：
1. 重定向：在定义路由的时候，可以加一个`redirect`参数，用来重定向的到另外一个页面。
2. 别名：在定义路由的时候，可以加一个`alias`参数，用来表示这个url的别名。以后也可以通过别名来访问到这个组件。


## 导航守卫：
### 全局导航守卫：
在`VueRouter`上实现的。总体来讲有两个函数，一个是`beforeEach`、`afterEach`。
1. `beforeEach(to,from,next)`：`to`代表的是上一个路由对象，`from`代表的是下一个路由对象。next代表的是控制下一步路由该怎么走。
  * next()：按照正常的流程来走。
  * next("/")：之前的路由被断掉了，重新走到/中去。
  * next(false)或者是没有调用：不会导向任何路由。
2. `afterEach(to,from)`：路由完成后的回调。

### 路由导航守卫：
在定义路由的时候，可以传递一个`beforeEnter(to,from,next)`参数来实现。里面的参数跟之前是一样的。

### 组件导航守卫：
1. `beforeRouteEnter(to,from,next)`：当前页面被进入之前调用。
2. `beforeRouteUpdate(fo,from,next)`：当前页面被复用了，参数改变了，会调用这个函数。
3. `beforeRouteLeave(fo,from,next)`：当前页面即将离开了，会调用这个。

### 导航守卫执行的流程：
1. 导航被触发。
2. 在失活的组件里调用离开守卫。
3. 调用全局的 beforeEach 守卫。
4. 在重用的组件里调用 beforeRouteUpdate 守卫 (2.2+)。
5. 在路由配置里调用 beforeEnter。
6. 解析异步路由组件。
7. 在被激活的组件里调用 beforeRouteEnter。
8. 调用全局的 beforeResolve 守卫 (2.5+)。
9. 导航被确认。
10. 调用全局的 afterEach 钩子。
11. 触发 DOM 更新。
12. 用创建好的实例调用 beforeRouteEnter 守卫中传给 next 的回调函数。