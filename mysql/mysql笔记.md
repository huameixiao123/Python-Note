# Mysql 数据库 

# 简介

关系型的数据库，流行，开源，免费，将数据保存在不同的表中，不是把数据存在一个大的仓库内，灵活性好
一张二维表来组织数据的，简单来说是以行和列来储存的，字段是表头
对大小写不敏感

# mysql操作 

- 进入mysql
`mysql -uroot -p`回车输入密码 

- 退出mysql
`\q` `exit`

- 创建用户
`create user 'username'@'%' identified by password;`  创建用户
`grant all on *.* to 'username'@'%';`	赋予用户权限
grant 权限 on 数据库.* to 用户名@登录主机 identified by "密码";　
`flush privileges;` 	刷新权限 使权限立即生效

- 查询当前用户 
`select user();`

- 修改指定用户密码
```
mysql>update mysql.user set password=password('新密码') where User="test" and Host="localhost";

mysql>flush privileges;
```
- 删除用户
```
mysql>Delete FROM user Where User='test' and Host='localhost';

 　　mysql>flush privileges;

 　　mysql>drop database testDB; //删除用户的数据库

删除账户及权限：>drop user 用户名@'%';

　　　　　　　　>drop user 用户名@ localhost; 
```


- 查询所有用户
` select user,host from mysql.user;`

- 进入数据库
`use databasename`

# 数据库的操作 

- 删除数据库
`drop database mydb;`

- 创建数据库
`create database [if not exists] mydb`

- 查询所有的数据库
`show databases;`

# 数据表的操作

- 创建表格
`create table [if not exists] table_name(field varchar(20),[...]);`

- 查看表结构
`desc table_name;`
`show create table table_name;`

- 查询当前数据库的表
`show tables`

- 删除表
`drop table table_name;`


# 表中的数据操作(CURD)

- 增加数据 
```
插入一条数据
inert [into] table_name(字段名) value(值);
插入多条数据
inert into table_name(字段名) values(值),(值);
如果不指定字段 默认全字段插入

insert [into] table_name set name=12,id=1;
```

- select
```
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M]

查询语句中你可以使用一个或者多个表，表之间使用逗号(,)分割，并使用WHERE语句来设定查询条件。
SELECT 命令可以读取一条或者多条记录。
你可以使用星号（*）来代替其他字段，SELECT语句会返回表的所有字段数据
你可以使用 WHERE 语句来包含任何条件。
你可以使用 LIMIT 属性来设定返回的记录数。
你可以通过OFFSET指定SELECT语句开始查询的数据偏移量。默认情况下偏移量为0。
```

- update
`UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause];`

- delete 
`DELETE FROM table_name [WHERE Clause];`

- where子句
```
SELECT field1, field2,...fieldN FROM table_name1, table_name2...
[WHERE condition1 [AND [OR]] condition2.....

查询语句中你可以使用一个或者多个表，表之间使用逗号, 分割，并使用WHERE语句来设定查询条件。
你可以在 WHERE 子句中指定任何条件。
你可以使用 AND 或者 OR 指定一个或多个条件。
WHERE 子句也可以运用于 SQL 的 DELETE 或者 UPDATE 命令。
WHERE 子句类似于程序语言中的 if 条件，根据 MySQL 表中的字段值来读取指定的数据。
```
- like子句

```
SELECT field1, field2,...fieldN 
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'

你可以在 WHERE 子句中指定任何条件。
你可以在 WHERE 子句中使用LIKE子句。
你可以使用LIKE子句代替等号 =。
LIKE 通常与 % 一同使用，类似于一个元字符的搜索。
你可以使用 AND 或者 OR 指定一个或多个条件。
你可以在 DELETE 或 UPDATE 命令中使用 WHERE...LIKE 子句来指定条件。
```
- union操作符
```
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
参数:
expression1, expression2, ... expression_n: 要检索的列。

tables: 要检索的数据表。

WHERE conditions: 可选， 检索条件。

DISTINCT: 可选，删除结果集中重复的数据。默认情况下 UNION 操作符已经删除了重复数据，所以 DISTINCT 修饰符对结果没啥影响。

ALL: 可选，返回所有结果集，包含重复数据。
```
- 排序
```
SELECT field1, field2,...fieldN table_name1, table_name2...
ORDER BY field1 [ASC [DESC][默认 ASC]], [field2...] [ASC [DESC][默认 ASC]]

你可以使用任何字段来作为排序的条件，从而返回排序后的查询结果。
你可以设定多个字段来排序。
你可以使用 ASC 或 DESC 关键字来设置查询结果是按升序或降序排列。 默认情况下，它是按升序排列。
你可以添加 WHERE...LIKE 子句来设置条件。
```

- 分组

```
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;
```

- 连接
```
INNER JOIN（内连接,或等值连接）：获取两个表中字段匹配关系的记录。
LEFT JOIN（左连接）：获取左表所有记录，即使右表没有对应匹配的记录。
RIGHT JOIN（右连接）： 与 LEFT JOIN 相反，用于获取右表所有记录，即使左表没有对应匹配的记录。
```

- 运算符
```
IS NULL: 当列的值是 NULL,此运算符返回 true。
IS NOT NULL: 当列的值不为 NULL, 运算符返回 true。
<=>: 比较操作符（不同于=运算符），当比较的的两个值为 NULL 时返回 true。
关于 NULL 的条件比较运算是比较特殊的。你不能使用 = NULL 或 != NULL 在列中查找 NULL 值 。

在 MySQL 中，NULL 值与任何其它值的比较（即使是 NULL）永远返回 false，即 NULL = NULL 返回false 。

MySQL 中处理 NULL 使用 IS NULL 和 IS NOT NULL 运算符。
```

- 查询条件支持正则表达式
```
查找name字段中以'st'为开头的所有数据：

mysql> SELECT name FROM person_tbl WHERE name REGEXP '^st';
查找name字段中以'ok'为结尾的所有数据：

mysql> SELECT name FROM person_tbl WHERE name REGEXP 'ok$';
查找name字段中包含'mar'字符串的所有数据：

mysql> SELECT name FROM person_tbl WHERE name REGEXP 'mar';
查找name字段中以元音字符开头或以'ok'字符串结尾的所有数据：

mysql> SELECT name FROM person_tbl WHERE name REGEXP '^[aeiou]|ok$';
```

- 







