### 入门

#### 创建mapper.xml文件、

```xml
<mapper namespace = "com.sc.pojo.Dept">
    <insert id = "addDept" parameterType = "String">
        insert into Dept(dname) values(#{dname})
    </insert>
    <select id = "selectDept" resultType="dept">
    	select * from Dept
    </select>
</mapper>
```

##### 设置别名

```xml
<typeAliases>
	<package name = "com.sc.pojo"/>
</typeAliases>
```

##### settings设置

```xml
--开启二级缓存
<settiings name = "cacheEnable" value = "true"/>
--级联使用
<settiings name = "lazyLoadingEnable" value="true"/>
```



#### environments环境配置

```xml
--加载配置属性文件
<properties resource="config.yaml">
<environments default="development">
    <environment id="development">
        <transactionManager type="JDBC"/>
        <dataSource type="POOLED">
            <property name="driver" value="${driver}"/>
            <property name="url" value="${url}"/>
            <property name="username" value="${username}"/>
            <property name="password" value="${password}"/>
        </dataSource>
    </environment>
</environments>
```

##### 事务管理器的配置

1. JDBC:这个配置直接使用了JDBC提交和回滚设施，它依赖从数据源获取的连接来管理事务作用域
2. Manager:让容器来管理事务的整个生命周期

##### 数据源的配置

1. unpooled,mybatis会为每一个数据库的操作创建一个新的连接，并关闭它
2. pooled，mybatis会创建一个数据库连接池，连接池的一个连接用于数据库操作。数据库操作完成后连接将返回连接池，适用于开发或者测试环境
3. JNDI:将从应用服务器的配置好的数据源获取数据库连接

#### mapper映射器

```xml
<mappers>
  <mapper class="org.mybatis.builder.AuthorMapper"/>
  <mapper class="org.mybatis.builder.BlogMapper"/>
  <mapper class="org.mybatis.builder.PostMapper"/>
</mappers>

<!-- 将包内的映射器接口实现全部注册为映射器 -->
<mappers>
  <package name="org.sc.mapper"/>
</mappers>
```

### Mapper映射文件详解

#### select查询

```xml
<select id = "selectDept" parameterType = "Integer" resultType="dept">
    --想要根据什么条件查询，就传入该参数的类型
    select * from Dept where deptno = #{id}
</select>
```

##### 命名空间标识符

1. resultType,返回的是集合，应该设置集合包含的类型，而不是集合本身的类型
2. resultMap:结果映射是mybatis最强大的特性
3. flushCache:为true时，都会导致本地缓存和二级缓存被清空，默认值为false
4. Cache:语句的结果将被二级缓存存起来，对select元素为true

##### 占位符的区别

1. #是预编译处理，mybatis会将#｛｝替换为？，并通过set方法进行赋值
2. $是字符串替换，会自动替换变量的值
3. #可以有效防止SQL注入，提高系统安全性

#### insert语句

```xml
<insert id = "insertAuthor" parameterType="author">
	insert into Author (id,username,password,email,bio)
    values(#{id},#{username},#{password},#{#email},#{bio})
</insert>
```

##### 标识符

1. flushCache:默认对insert、update、delete语句为true

##### 主键自增语句

```xml
--支持自动生成主键的字段
<insert id="insertAuthor" useGeneratedKeys="true"
    keyProperty="id">
  insert into Author (username,password,email,bio)
  values (#{username},#{password},#{email},#{bio})
</insert>
```

#### update、delete语句

```xml
<update id="updateAuthor" parameterType="author">
  update Author set
    username = #{username},
    password = #{password},
    email = #{email},
    bio = #{bio}
  where id = #{id}
</update>

<delete id="deleteAuthor" parameterType="int">
  delete from Author where id = #{id}
</delete>
```

### MyBatis代理层开发Dao层

##### 编写mapper接口规范

1. 接口名和映射名相同且在同一个包下
2. 在映射文件中，namespace="完全包名.接口名"
3. 接口的方法名和statement中的id一致
4. 接口的参数/返回参数和statement中的参数/resultType一致

##### 测试

```java
InputStream inputStream = Resources.getResourceAsStream("SqlConfig.xml");
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder.built(inputStream);
@Test
public void test() throw Exception {
    SqlSession session = sqlSessionFactory.openSession();
    DeptMapper deptMapper = session.getMapper("DeptMapper.class");
    Dept dept = deptMapper.selectById("3");
    
}
```

### 动态SQL

##### if实现查询功能

```xml
<if test = "sal != null">
	and sal > 3000
</if>
```

##### if+where标签

```xml
<where>
	<if test = "name != null">
        name like '%name%'
    </if>
    <if test = "sal != null">
    	and sal < 6000
    </if>
</where>
```

##### choose+when+otherwise

```xml
<choose>
	<when test = "xx">
    	and xxxxx
    </when>
    <when test = "yyy">
    	and
    </when>
    <otherwise>
    	xxx
    </otherwise>
</choose>
```

##### **trim+if标签**

```xml
//与where相似，但是prefixOverrides会自动将指定的词消除，加入prefix
<trim prefix="where" prefixOverrides="and || or">
    
</trim>
<trim prefix="(" suffix=")" suffixOverrides=","></trim>
```



##### set + if + where

```xml
<set>
    <if></if>
</set>
<where>
    <if></if>
</where>
```

##### foreach

```xml
<foreach collection = "list" item = "item" open = "(" close=")" separator=",">
    #{no}
</foreach>
```

##### SQL片段

```xml
<sql id = "selectId">
    select * from emp
</sql>
//应用
<select>
	<include refid="selectId"/>
</select>
```

##### bind元素

```xml
 <select id="selectEmpBysalename" parameterType="emp" resultType="emp">
        <bind name="name" value="'%' + ename + '%'"/>
        select * from emp
        <where>
            <if test="sal !=null ">
                and  sal <![CDATA[ <= ]]>#{sal}
            </if>
            <if test="ename != null">
                and ename like #{name}
            </if>
        </where>
    </select>
```

### Mybatis查询

#### 一对一关联查询

##### 使用resultMap属性

```xml
--type:指的是返回的类型 
<resultMap type="com.msb.pojo.Emp" id="EmpAndDept">
       <id column="empno" property="empno"/>
       <result column="ename" property="ename"/> 
       <result column="mgr" property="mgr"/>
       <result column="sal" property="sal"/>
       <result column="hiredate" property="hiredate"/>
       <association property="dept" javaType="com.msb.pojo.Dept">
           <id column="deptno" property="deptno"/>
           <result column="dname" property="dname"/>
           <result column="loc" property="loc"/>
       </association>
   </resultMap>

   <select id="findAll" resultMap="EmpAndDept"> 
        select e.empno,e.ename,e.mgr,e.sal,e.hiredate,d.deptno,d.dname,d.loc
        from emp e  inner join dept d 
                    on e.deptno=d.deptno 
   </select>
```

##### 相关案例:查询部门所有的信息及部门下的所有员工信息

```xml
 <resultMap type="com.msb.pojo.Dept" id="DeptAndEmps">
	   <id column="deptno" property="deptno"/>
	   <result column="dname" property="dname"/>
	   <result column="loc" property="loc"/>
	   <collection property="emps" ofType="com.msb.pojo.Emp">
	         <id column="empno" property="empno"/>
	         <result column="ename" property="ename"/>
	         <result column="sal" property="sal"/>
	   </collection>
 </resultMap>
 <select id="findDeptByid" parameterType="int" resultMap="DeptAndEmps">
    select d.deptno,d.dname,d.loc,e.empno,e.ename,e.sal
    from dept d inner join emp e on d.deptno=e.deptno
    where d.deptno=#{id}

 </select>
```

测试

```java
@Test//部门含有员工的集合信息
public void test1(){
		SqlSession session =factory.openSession();
		DeptMapper deptmapper= session.getMapper(DeptMapper.class);
		Dept dept=deptmapper.findDeptByid(10);
		
		System.out.println("部门信息："+dept.getLoc()+";"+dept.getDname()+";"+dept.getLoc());
		System.out.println("部门里，所有员工的信息：");
		for(Emp e:dept.getEmps()){
			System.out.println(e.getEname()+";"+e.getEmpno()+";"+e.getSal());
		}
		session.close();
	}
```

#### 多对多关联查询

##### 查询所有用户订单里的所有商品信息



#### 使用分页查询

ROWBOUNDS插件

```java
List<User> findAll(RowBounds rb);
/**映射文件
<select id = "findAll" resultType("user") {
	select * from user;
}
*/
RowBounds rb=new RowBounds(0, 2);
List<User> list=usermapper.findall( rb);
```

### 延迟加载

#### 延迟加载配置

```xml
<settings>
	<setting name = "lazyLoadingEnabled" value = "true"/>
    <setting naeme = "aggressiveLazyLoading" value = "true"/>
</settings>
```

aggressiveLazyLoading:开启式时，访问对象中一个懒属性时，将完全加载这个懒属性的所有懒属性，false按需加载对象属性

### MyBatis缓存机制

#### mybatis一级缓存

1. Mybatis默认一级缓存，不需要在配置文件里配置
2. 同一个session作用域里，第二次进行相同查询的时候，直接获得缓存数据
3. 同一个session，获得session对象开始到session.commit或session.close或session.flush结束



#### mybatis二级缓存

1. mapper范围级别
2. 配置文件开启：<setting name="cacheEnabled" value="true"/>  
3. 单独映射文件:<cache type="org.mybatis.caches.ehcache.EhcacheCache"/>
4. 实现序列化

补充：

1. 禁用二级缓存：useCache="false",默认查询语句为true，在对应查询修改即可
2. 刷新缓存：flushCache="false",在mapper的同一个namespace中，如果有其它insert，update,delete操作数据后需要刷新缓存，如果不执行刷新缓存会出现脏读
3. 说明:在一级缓存中执行sessoion.commit。即使设置了flushCache="false"也会刷新，二级缓存不会

#### Mybatis整合第三方框架

##### 分布式缓存框架：

1. 使用分布式部署（集群部署方式）
2. 缓存的数据在各个服务单独存储，不方便系统开发，使用分布式缓存对数据进行集中管理
3. ehache、redis、memcache缓存框架

Ehache:

1. 是一种广泛使用的开源Java分布式缓存。主要面向通用缓存，JavaEE和轻量级容器。它具有内存和磁盘存储功能
2. 被用于大型复杂分布式web application

##### 实现步骤：

1. mybatis-ehache
2. 配置文件添加`:<setting name="cacheEnabled" value="true"/>`  
3. 对应的映射文件开启:<cache type="org.mybatis.caches.ehcache.EhcacheCache"/>
4. 实体类实现序列化





###  + 