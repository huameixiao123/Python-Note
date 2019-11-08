# 安装 
```sehll
sudo apt install redis-server

ps aux | grep redis

sevice redis stop

service redis start

redis-cli -h [ip] -p [port]

```

# 数据类型

## 字符串
```shell

set key value  # 如果字符串中有空格，使用双引号

del key # 删除一条数据

set key value EX 10 # 设置过期时间 

ttl key  # 查看键的过期时间

expire key 10 # 设置过期时间

keys *  # 查看所有的key

flushall # 清楚所有键值对

```

## 列表
key对应的value是列表类型 []
```shell

lpush key value  # 在列表左边添加元素

rpush key value  # 在列表右边添加元素

lrange key start stop  # 查看列表数据

lpop key # 左边删除

rpop key # 右边删除

lrem key count value # 移除并返回列表key的中间元素 

lindex key index # 索引取值

llen key # key中的元素个数

lrem key count value # 删除列表中相同个数的元素 count=0 表示删除全部个数 count>0 表头搜索 count<0 表尾搜索
```

## 集合
key对应的value的类型是集合 {} 无序的 元素唯一 

```shell

sadd set key value  # 添加元素 

smembers key # 查看元素 

srem key # 移除key

scard key # 查看集合中的元素个数

sinter key1 key2 # 集合交集

sunion key1 key2 # 集合并集

sdiff key1 key2 # 集合差集 key1 - key2
```
## 哈希
key 对应的value的类型是哈希 类似于dict格式

```shell
hset key field value  # 添加数据

hget key field  # 获取数据

hdel key field  # 删除数据

hgetall key # 获取所有哈希数据

hkeys key # 获取hash中所有的field

hvals key # 获取hash中所有的value

hexits key field # 判断hash中是否存在field

```
## 事务操作
原子性
隔离性

```shell

multi # 开启事务

exec  # 执行事务

discard # 取消事务 

watch key1 key2 # 监视一个或者多个key 在事务执行之前 对key进行监视 key发生改变的话，事务不会执行

unwatch # 全部取消监视

```


## 发布和订阅操作

```shell
publish channel message # 发布频道消息

subscibe channel # 订阅频道 可以订阅多个频道
```

## 数据持久

redis提供了2种数据保存的方式 RDB 和 AOF

### RDB同步机制

1. 开启和关闭：默认情况下是开启了。如果想关闭，那么注释掉`redis.conf`文件中的所有`save`选项就可以了。
2. 同步机制：
    * save 900 1：如果在900s以内发生了1次数据更新操作，那么就会做一次同步操作。
    * save 300 10：如果在300s以内发生了10数据更新操作，那么就会做一次同步操作。
    * save 60 10000：如果在60s以内发生了10000数据更新操作，那么就会做一次同步操作。
3. 存储内容：具体的值，不是命令。并且是经过压缩后存储进去的。
4. 存储路径：根据`redis.conf`下的`dir`以及`rdbfilename`来指定的。默认是`/var/lib/redis/dump.rdb`。
5. 优点：
    * 存储数据到文件中会进行压缩，文件体积比aof小。
    * 因为存储的是redis具体的值，并且会经过压缩，因此在恢复的时候速度比AOF快。
    * 非常适用于备份。
6. 缺点：
    * RDB在多少时间内发生了多少写操作的时候就会出发同步机制，因为采用压缩机制，RDB在同步的时候都重新保存整个Redis中的数据，因此你一般会设置在最少5分钟才保存一次数据。在这种情况下，一旦服务器故障，会造成5分钟的数据丢失。
    * 在数据保存进RDB的时候，Redis会fork出一个子进程用来同步，在数据量比较大的时候，可能会非常耗时。

### AOF同步机制：
1. 开启和关闭：默认是关闭的。如果想要开启，那么修改redis.conf中的`appendonly yes`就可以了
2. 同步机制：
    * appendfsync always：每次有数据更新操作，都会同步到文件中。
    * appendfsync everysec：每秒进行一次更新。
    * appendfsync no：使用操作系统的方式进行更新。普遍是30s更新一次。
3. 存储内容：存储的是具体的命令。不会进行压缩。
4. 存储路径：根据`redis.conf`下的`dir`以及`appendfilename`来指定的。默认是`/var/lib/redis/appendonly.aof`。
5. 优点：
    * AOF的策略是每秒钟或者每次发生写操作的时候都会同步，因此即使服务器故障，最多只会丢失1秒的数据。 
    * AOF存储的是Redis命令，并且是直接追加到aof文件后面，因此每次备份的时候只要添加新的数据进去就可以了。
    * 如果AOF文件比较大了，那么Redis会进行重写，只保留最小的命令集合。
6. 缺点：
    * AOF文件因为没有压缩，因此体积比RDB大。 
    * AOF是在每秒或者每次写操作都进行备份，因此如果并发量比较大，效率可能有点慢。
    * AOF文件因为存储的是命令，因此在灾难恢复的时候Redis会重新运行AOF中的命令，速度不及RDB。

## 设置密码 

1. 设置密码：在`reids.conf`配置文件中，将`requirepass pasword`取消注释，并且指定你想设置的密码。
2. 使用密码连接reids：
    * 先登录上去，然后再使用`autho password`命令进行授权。
    * 在连接的时候，通过`-a`参数指定密码进行连接。

## python操作redis

## 远程连接redis

如果想要让其他机器连接本机的redis服务器，那么应该在`redis.conf`配置文件中，指定`bind 本机的ip地址`。这样别的机器就能连接成功。不像是网上说的，要指定对方的ip地址。
