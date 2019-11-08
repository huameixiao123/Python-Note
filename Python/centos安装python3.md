# centos7安装python3.6同时保留python2.7

## 安装python3.6
1. 下载python3.6源码安装包。地址`https://www.python.org/downloads/release/python-360/`
2. 使用`tar -xvzf Python-3.6.0.tgz`解压
3. 进入Python-3.6.0目录进行安装，执行`./configure --prefix=/usr/local/python3` 指定安装目录，依次执行`make`和`make install`安装

## 修改yum配置文件的参数指向原python2.7，这样就不影响系统原来的依赖关
系。
1. `vi /usr/bin/yum`
2. 修改第一行 `#!/usr/bin/python` 为 `#!/usr/bin/python2`保存退出。

## 在`usr/bin`目录建立新的`python`链接文件到`python3.6`，以便可以快捷执行`python3.6`
1. 删除原python连接文件 `rm /usr/bin/python`
2. 重新建立连接文件 `ln -s /usr/local/python3/bin/python3.6 /usr/bin/python`
