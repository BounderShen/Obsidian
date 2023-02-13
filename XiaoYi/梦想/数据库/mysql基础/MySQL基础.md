#### MYSQL概述
##### 命令行方式
1. net start MySQL57
2. net stop MySQL57
##### 客户端服务器
1. 如果你使⽤的是类Unix系统，并且省略 -u 参数后，会把你登陆操作系统的⽤⼾名当作 MySQL 的 ⽤⼾名去处理
2. \g或\G或回⻋结束，\G以垂直的⽅式返回结果
3. \c：放弃本次操作
#### 浮点类型
##### 设置最大位数和最小位数
1. FLOAT(M，D)
2. Double(M,D)
3. M:表示该数值需要最多的十进制有效位数
4. D：小数点后的十进制数字个数
##### 定点数类型
1. DECIMAL(M,D)
#### 数据库的基本操作
##### 创建数据库
1. create database if not exists xxx
2. 可以在启动的时候在后面直接加数据库的名称
##### 删除数据库
1. drop database xxx
2. drop database if exists xxx
##### 表的基本操作
1. 创建表语句
`sql
create table tableName (
first_column int)`
##### 为建表语句添加注释
1. 在创建表后面的语句添加：comment ‘xx’
##### 删除表
1. drop table tableName,tableName2;
##### 查看表结构
1. desc tableName;
2. show creata table tableName;
##### 修改表名
1. alter table odlTalbeName to newTableName;
2. rename table tableName1 to tableName2, talbeName3 to tableName3;
##### 增加列
1. alter table tableName add colucmn ColumnName dataType attribute;
2. 添加到指定位置：first 或者after xxx
##### 删除列
1. alter table tableName drop column columnTalbe;
##### 修改列信息
1. alter table tableName modify 列名 新数据类型 新属性；
2. alter tableName talbeName change 列名 新数据类型 新属性
##### 修改列的位置
1. alter table tableName modify 列名 列的类型 列的属性 first
##### 一条语句中包含多个修改操作
1. alter table tableName 操作1，操作2，
#### 列的属性
##### 简单插入语句
1. insert into tableName(列名，列名2) values(值1，值2)
2. 没有显式子指定的列值，为NULL
##### 批量插入
1. values的后面使用逗号进行分隔开
##### 默认值
1. 列名 列类型 default 默认值
##### NOT NULL属性
1. 列名 列类型 NOT NULL
##### 主键
1. 列名 列类型 primary key
2. 可提取出来，primary key (列名1，)
##### UNIQUE属性
1. 不允许重复
2. UNITQUE KEY 约束名称 (列名) ，多个列的组合具有UNIQUE必须单独声明
##### 主键和约束的区别
1. 一张表可以拥有多张主键，却可以定义多个UNIQUE约束
2. UNIQUE可以允许为NULL，却可以重复多条记录
##### 外键
1. CONSTRAINT 外键名称 FOREIGN KEY(列1，列2) references 父表名(列名)
2. 使用外键，父表中的所依赖的列必须建立了索引
##### AUTO_INCREMENT
1. 列名 列类型 AUTO_INCREMENT
2. 添加新纪录没有不指定该列的值，或者显式指定该列的值为NULL或者0
3. 一个表中最多具有一个AUTO_INCREMENT
4. 拥有这个属性的列必须建立索引
5. 拥有这个属性就不可以添加default
6. 一般使用AUTO_INCREMENT都是作为主键的属性，来生成唯一标识的
##### 列的注释
1. 在列后面添加 comment  ''
##### 影响外观展示的ZEROFILL属性
1. int(10) unsigned zerofill
2. zerofill表示会补充o,假如为1会在前面补充9个0
3. 补充0的条件
	1. 整数类型
	2. 具有UNSIGNED ZEROFILL属性
	3. 实际值必须小于宽度
##### 一个列可以具有多个属性
1. 可以具有多个但是不能冲突