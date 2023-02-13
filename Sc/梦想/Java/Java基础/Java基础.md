### 封装

##### 好处

1. 实现精准控制

### 继承

##### 注意

1. 子类拥有父类非private的属性和方法
2. 子类可以拥有自已的方法和属性（扩展）
3. 子类可以用自已的方式实现父类的方法（重写）

#### 构造器

1. 默认调用父类构造器的前提，父类有默认构造器

#### protected关键字

对于protected而言，它指明就类用户而言，他是private，但是对于任何继承与此类的子类而言或者其他任何位于同一个包的类而言，他是可以访问的

####  谨慎继承

1. 父类变，子类变
2. 继承破坏了封装，对于父类而言你，它的实现细节对于子类来说是透明的
3. 继承是一种强耦合关系
4. 是否需要向上转型，如果不需要则应当好好考虑自已是否需要继承

### 多态

```java
public class Wine {
    public void fun1() {
        System.out.println("Wine 的Fun....");
        fun2();
    }
    public void fun2() {
        System.out.println("Wine 的fun2");
    }
}
public class JNC extends Wine {

    public void fun1(String a) {
        System.out.println("JNC fun1");
        fun2();
    }
    @Override
    public void fun2() {
        System.out.println("JNC fun2");

    }
}
public class Test {
    public static void main(String[] args) {
        Wine w = new JNC();
        w.fun1();
    }
}
//运行结果调用父类的fun1,后调用子类的fun2
```

指向子类的父类是向上转型，它只能访问父类拥有的属性和方法，而对子类中存在而父类不存在的方法，该引用是不能使用的，尽管是重载该方法。若子类重写了父类中的某些方法，在调用这些方法的时候，必定是使用子类中定义的这些方法（动态连接、动态调用）

#### 多态的实现

##### 实现条件

1. 重写、向上转型
2. 多态的实现机制原则：当超类对象引用子类对象时，被调用的方法必须是子类覆盖的方法

##### 实现形式

1. 接口、继承、多态

#### 基于继承实现的多态

对于引用子类的父类类型，处理该引用时，它适用于继承该父类的所有子类、子类对象的不同，对方法的实现也就不同，执行相同动作产生的行为也就不同

#### 基于接口实现的多态

1. 在接口的多态中，指向接口的引用必须是指定这实现了该接口的一个类的实例程序，在运行时，根据对象引用的实际类型来执行对象的方法

```java
public class A {
    public String show(D obj) {
        return ("A and D");
    }

    public String show(A obj) {
        return ("A and A");
    }

}

public class B extends A{
    public String show(B obj){
        return ("B and B");
    }

    public String show(A obj){
        return ("B and A");
    }
}

public class C extends B{

}

public class D extends B{

}

public class Test {
    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new B();
        B b = new B();
        C c = new C();
        D d = new D();

        System.out.println("1--" + a1.show(b));
        System.out.println("2--" + a1.show(c));
        System.out.println("3--" + a1.show(d));
        System.out.println("4--" + a2.show(b));
        System.out.println("5--" + a2.show(c));
        System.out.println("6--" + a2.show(d));
        System.out.println("7--" + b.show(b));
        System.out.println("8--" + b.show(c));
        System.out.println("9--" + b.show(d));
    }
}
1--A and A
2--A and A
3--A and D
//为什么是B and A:因为a2的实例对象是指向子类的父类向上转型，只能使用父类的属性它只能访问父类拥有的属性和方法，而对子类中存在而父类不存在的方法，该引用是不能使用的，尽管是重载该方法。
4--B and A
5--B and A
6--A and D
7--B and B
8--B and B
9--A and D
```

### 抽象类与接口

#### 抽象类

1. 抽象类不能被实例化，实例化由子类完成，它只需要一个引用即可
2. 抽象方法必须由子类重写
3. 只要包含一个抽象方法就是抽象类
4. 子类中的抽象方法不能与父类抽象方法同名
5. abstract不能与final修饰同一个类
6. abstract不能与private、static、final或final并列修饰同一个方法

#### 接口

1. 接口中可以定义不可变的常量，接口中的成员变量会自动变为<u>public static final</u> ，通过ImplementClass.name
2. 实现接口的非实现类必须要实现该接口的所有方法，抽象类可以不用实现
3. 不能用new操作符实例化一个接口，但可以声明一个接口变量，该变量必须引用一个实现该接口的类的对象。
4. 实现多接口的时候一定要避免方法名的重复

#### 抽象类与接口的区别

##### 语法层次

抽象类方式，可以拥有任意范围的成员数据，同时可以拥有自已的非抽象方法，但接口只能有静态、不能修改的成员数据，且方法必须是抽象的

##### 设计层次

1. 抽象类是对类的抽象，接口是行为的抽象
2. 跨域不同。抽象类只能跨域相似特点的类，而接口可以跨域不同的类
3. 设计层次不同。对于抽象类，它是自上而下的设计

### 关键字static

#### static变量

1.  static变量置于方法区中。
2. 在类中用static 声明的成员变量为静态成员变量，它为该类的公用变量，在第一次使用时初始化，对于该类的所有对象来说，static成员变量只有一份

#### static方法

1. 调用该方法时，不会将对象的引用传递给它，所以在static方法中不可以访问非static的成员变量

#### 静态初始化块

##### Java类的执行顺序

1. 该类的静态变量
2. 该来的静态初始化块
3. 该类的构造器

##### 父类的执行顺序

1. 父类的静态变量
2. 父类的静态代码块
3. 子类的静态变量
4. 子类的静态代码块

#### 内存分析Static

1. 除了8种基本数据类型，其他都是引用
2. 堆是存储对象，但是对象如果有引用类型那么它的值会存储在数据，在堆中存储的是地址，
3. 数据区可以存储静态成员变量、堆引用类型的值

### String性质深入解析

#### String的不可变性

##### final类和final类的私有成员

1. 使用数组创建String时，是复制了数组来进行创建

##### 改变即创建创建对象的方法

1. subString: 

   ```java
   ((beginIndex == 0) && (endIndex == value.length)) ? this : new String(value,beginIndex,subLen);
   ```

2. replace、repalceAll()

#### 字符串拼接

##### 使用+拼接字符串

```java
String s = "Love You";
String s2 = "Love"+" You";
String s3 = s2 + "";
String s4 =  new String("Love You");
//反编译后
String s3 = (new StringBuilder(String.valueOf(s2))).toString();
System.out.println((new StringBuilder("s == s2")).append(s == s2).toString());
```

1. s、s2常量表达式计算就是在编译期间完成的
2. s3，运行时计算结果并在堆创建对象’
3. s4直接在堆中创建对象
4. 运行期间的+计算是通过创建StringBuilder对象，调用append()方法来完成的

##### concat

```Java
public String concat(String str) {
    int otherLen = str.length();
    if (otherLen == 0) {
        return this;
    }
    int len = value.length();
    char[] buf = Arrays.copyOf(value,len+otherLen);
    //将str复制进buf数组
    str.getchars(buf,len);
    return new String(buf,true);
    
}
```

#### StringBuffer和StringBuilder

1. 循环体内使用+会反复地创建StringBuilder对象来进行拼接，造成内存浪费，耗时间
2. 并发场景使用StringBuffer替代StringBuilder

### 深入剖析Java中的装箱和拆箱

#### 基本数据类型

##### 优点

1. 直接在栈内存中存储，

##### 超出范围

1. 溢出的时候不会抛出异常，也没有任何提示，所以同类型计算的时候注意数据溢出的问题

#### 包装类型

##### 优点

1. Java是面向对象语言，很多需要使用的是对象
2. 是数据具有对象的性质，并且为其添加了属性和方法，丰富了基本类型的操作

##### 自动拆箱与装箱

```java
//原理
Integer interger = 1;
int i = interger;
//反编译后
Integer integer = Integer.valueof(1);
int i = integer.intValue();
```

##### 装拆箱的场景

1. 将基本数据类型放入集合累

2. 包装类型和基本类型的比较

3. 包装类型的运算

4. 三目运算符的使用

5. 函数参数与返回值

   ```java
   public int getNum(Integer num) {
       return num;
   }
   public Integer getNum(int num) {
       return num;
   }
   ```

#### 自动装拆箱与缓存

1. 通过使用相同的对象引用实现了缓存和重用

2. 适用于装箱

3. ```java
   -128到127
   true 和 false
   '\u0000'到'\u007f'之间的字符
   ```

#### 自动拆装箱带来的问题

1. -128～127的数字可以直接比较，范围之外需要equals比较
2. 如果包装对象为null，自动拆箱会抛出NPE
3. 一个for循环大量拆装箱操作会浪费很多资源

### 深入解析Java四种访问权限

#### 访问权限控制使用的场景

##### 外部类的访问控制

1. 嵌套类而言，外部类的访问控制只能是public、default

##### 类里面的成员的访问控制

1. 类里面的访问控制可以四种
2. 局部成员没有访问权限控制，因为局部成员变量只在作用域内起作用

##### 抽象方法的访问权限

1. 普通方法可以拥有四种，但抽象方法不能用private来修饰

##### 接口成员的访问权限

1. 变量:public static final
2. 抽象方法:public abstract
3. 静态方法:public static 1.8之后
4. 内部类、内部接口:public static
5. 默认强制规定好，可以少写，但不能写错

##### 构造器访问权限

1. 采用private: 一般是不允许直接构造这个类的对象，再结合工厂方法(static)，实现单例模式。所有子类都不能继承
2. 包访问控制:这个类的对象只能在本 包使用，但是这个类有static成员，那么这个类还是可以在外包使用的
3. 注意:子类的构造器初始化时都要调用父类的构造器，一旦父类构造器不能被访问，那么子类的构造器调用失败，意味子类继承父类失败

### 深入分析Java的序列化和反序列化

#### Java对象的序列化

Java平台允许我们在内存中创建可复用的Java对象，但一般情况下，只有当JVM处于运行时，这些对象才可能存在，即，这些对象的生命周期不会比JVM的生命周期更长。但在现实应用中，就可能要求在JVM停止运行之后能够保存(持久化)指定的对象，并在将来重新读取被保存的对象。Java对象序列化就能够帮助我们实现该功能。

使用Java对象序列化，在保存对象时，会把其状态保存为一组字节，在未来，再将这些字节组装成对象。必须注意地是，对象序列化保存的是对象的”状态”，即它的成员变量。由此可知，对象序列化不会关注类中的静态变量。

#### 如何对Java对象进行序列化和反序列化

##### 对对象的序列化和反序列化

```java
public class SerializableDemo {
    //创建一个实现序列化的对象
    ObjectOutputStream oos = null;
    try {
        oos = new ObjectOutputStream(new FileOutputStream("tempFile"));
        oos.writeObject(user);
        
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        IOUtils.closeQuietly(oos);
    }
    File file = new File("tempFile");
    ObjectInputStream ois = null;
    try {
        ois = new ObjectInputStream(new FileInputStream(file));
        User newUser = (User) ois.readObject();
        System.out.println(newUser);
    } catch (IOException e) {
        e.printStackTrace();
    } catch (ClassNotFoundException e) {
        e.printStackTrace();
    } finally {
        IOUtils.closeQuietly(ois);
        try {
            FileUtils.forceDelete(file);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
}
```

#### 序列化及反序列化相关知识

1. 只要实现序列化接口，那么它就可以被序列化
2. 通过ObjectOutputStream和ObjectInputStream对对象进行序列化及反序列化
3. 虚拟机是否允许序列化，不仅取决于类路径和功能代码是否一致，一个非常重要的一点是两个类的序列化ID是否一致（private static final serialVersionUID）
4. 序列化并不保存静态变量
5. 要想将父类对象也序列化，就需要让父类对象也实现序列化接口
6. Transient关键字是控制变量的序列化，在变量加这个，可以阻止该变量被序列化到文件中，在被反序列化后，transient变量的值被设为初始值，如int 是 o，对象是null
7. 服务器端给客户端发送序列化对象数据，对象中有一些数据是敏感的，比如密码字符串等，希望对该密码字段在序列化时，进行加密，而客户端如果拥有解密的密钥，只有在客户端进行反序列化时，才可以对密码进行读取，这样可以一定程度保证序列化对象的数据安全。

#### ArrayList的序列化

##### writeObject和readObject方法

在ArrayList中定义了两个方法:writeObject和readObject方法

结论：序列化过程中，如果被序列化的类中定义了writeObject和readObject方法，虚拟机会试图调用对象类里的writeObject和readObject方法，进行用户自定义的序列化和反序列化。如果没有则调用ObjectOutputStream 的 defaultWriteObject 方法以及 ObjectInputStream 的 defaultReadObject 方法。

用户自定义的 writeObject 和 readObject 方法可以允许用户控制序列化的过程，比如可以在序列化的过程中动态改变序列化的数值。

### why transient

ArrayList实际上是动态数组，每次在放满以后自动增长设定的长度值，如果数组自动增长长度设为100，而实际只放了一个元素，那就会序列化99个null元素。为了保证在序列化的时候不会将这么多null同时进行序列化，ArrayList把元素数组设置为transient

### why writeObject and readObject

为了防止一个包含大量空对象的数组被序列化，为了优化存储，所以，ArrayList使用`transient`来声明`elementData`。 但是，作为一个集合，在序列化过程中还必须保证其中的元素可以被持久化下来，所以，通过重写`writeObject` 和 `readObject`方法的方式把其中的元素保留下来。

`writeObject`方法把`elementData`数组中的元素遍历的保存到输出流（ObjectOutputStream）中。

`readObject`方法从输入流（ObjectInputStream）中读出对象并保存赋值到`elementData`数组中。

##### 如何自定义的序列化和反序列化策略

可以通过在被序列化的类中增加writeObject 和 readObject方法。

##### 如果一个类中包含writeObject 和 readObject 方法，那么这两个方法是怎么被调用的?

在使用ObjectOutputStream的writeObject方法和ObjectInputStream的readObject方法时，会通过反射的方式调用。

#### 总结

1. 如果一个类想被序列化，需要实现Serializable接口。否则将抛出`NotSerializableException`异常，这是因为，在序列化操作过程中会对类型进行检查，要求被序列化的类必须属于Enum、Array和Serializable类型其中的任何一种。
2. 在类中增加writeObject 和 readObject 方法可以实现自定义序列化策略

### Java序列化的高级认识

#### 序列化ID问题

序列化ID不同，无法相互序列化和反序列化

#### 静态变量序列化

序列化保存的是对象的状态，而静态变量的类的状态

#### 对敏感字段加密

 **情境：**服务器端给客户端发送序列化对象数据，对象中有一些数据是敏感的，比如密码字符串等，希望对该密码字段在序列化时，进行加密，而客户端如果拥有解密的密钥，只有在客户端进行反序列化时，才可以对密码进行读取，这样可以一定程度保证序列化对象的数据安全。

##### 加密密码

```java
private void readObject(ObjectInputStream in) {
        try {
            ObjectInputStream.GetField readFields = in.readFields();
            Object object = readFields.get("password", "");
            System.out.println("要解密的字符串:" + object.toString());
            //模拟解密,需要获得本地的密钥
            password = "pass";
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
    private void writeObject(ObjectOutputStream out) {
        try {
            ObjectOutputStream.PutField putFields = out.putFields();
            System.out.println("原密码:" + password);
            //模拟加密
            password = "encryption";
            putFields.put("password", password);
            System.out.println("加密后的密码" + password);
            out.writeFields();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```

#### 序列化存储规则

##### 存储规则问题的代码

```java
ObjectOutputStream out = new ObjectOutputStream(
                new FileOutputStream("result.obj"));
Test test = new Test();
//试图将对象两次写入文件
out.writeObject(test);
out.flush();
System.out.println(new File("result.obj").length());
out.writeObject(test);
out.close();
System.out.println(new File("result.obj").length());
ObjectInputStream oin = new ObjectInputStream(new FileInputStream(
        "result.obj"));
//从文件依次读出两个文件
Test t1 = (Test) oin.readObject();
Test t2 = (Test) oin.readObject();
oin.close();
//判断两个引用是否指向同一个对象
System.out.println(t1 == t2);
```

总结:Java序列化机制为了节省磁盘空间，具有特定的存储规则，当写入文件的为同一对象时，并不会再将对象的内容进行存储，而是再次存储一份引用，增加的5字节存储空间就是新增引用和控制信息。反序列化时，恢复引用关系，使得清单中的两个对象指向唯一的对象，二者相等。极大的节省了存储空间

##### 特性案例分析

```java
ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("result.obj"));
Test test = new Test();
test.i = 1;
out.writeObject(test);
out.flush();
test.i = 2;
out.writeObject(test);
out.close();
ObjectInputStream oin = new ObjectInputStream(new FileInputStream(
                    "result.obj"));
Test t1 = (Test) oin.readObject();
Test t2 = (Test) oin.readObject();
System.out.println(t1.i);
System.out.println(t2.i);
```

总结：目的是将修改前后的对象存储进去，结果两个输出的都是 1， 原因就是第一次写入对象以后，第二次再试图写的时候，虚拟机根据引用关系知道已经有一个相同对象已经写入文件，因此只保存第二次写的引用，所以读取时，都是第一次保存的对象。读者在使用一个文件多次 writeObject 需要特别注意这个问题。

### 反射

#### 概念

Java反射机制是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为Java语言的反射机制

##### 如何理解反射？

每一个类，可以调用getClass方法获取对应的class对象，用来描述目标类，我们将这个class类叫做目标类的运行时类

##### Class对象，可以做什么

调用Class的对象的newInstance方法，可以动态创建目标类的对象

1. 目标类必须有无参数构造方法
2. 外部方法有足够的权限访问目标类的构造方法
3. 反射可以调用对象的各种方法，访问成员变量

##### Java反射机制用途

1. 在运行时判断对象所属的类
2. 在运行时构造任意一个类的对象
3. 在运行时判断任意一个类所具有的成员变量和方法
4. 在运行时调用任意一个对象的方法

#### 反射相关的主要API

**Class的常用方法：**

| 方法                                              | 描述                           |
| ------------------------------------------------- | ------------------------------ |
| public Class<?>[] getInterfaces()                 | 返回运行时类实现的全部接口。   |
| public Class<? Super T> getSuperclass()           | 返回运行时类的父类。           |
| public Constructor<T>[] getConstructors()         | 返回运行时类的public构造方法。 |
| public Constructor<T>[] getDeclaredConstructors() | 返回运行时类的全部构造方法。   |
| public Method[] getMethods()                      | 返回运行时类的public方法。     |
| public Method[] getDeclaredMethods()              | 返回运行时类的全部方法。       |
| public Field[] getFields()                        | 返回运行时类的public成员变量。 |
| public Field[] getDeclaredFields()                | 返回运行时类的全部成员变量。   |

**Method的常用方法：**

| 方法                                  | 描述                       |
| ------------------------------------- | -------------------------- |
| public Class<?> getReturnType()       | 返回方法的返回值类型。     |
| public Class<?>[] getParameterTypes() | 返回方法的参数列表。       |
| public int getModifiers()             | 返回方法的访问权限修饰符。 |
| public String getName();              | 返回方法名。               |

**Field的常用方法：**

| 方法                      | 描述                           |
| ------------------------- | ------------------------------ |
| public int getModifiers() | 返回成员变量的访问权限修饰符。 |
| public Class<?> getType() | 返回成员变量的数据类型。       |
| public String getName()   | 返回成员变量的名称。           |

#### 反射的应用

反射在实际中应用主要是动态创建对象，动态调用对象的方法

1. 调用Class的newInstance方法创建对象
2. 调用指定方法
   1. 通过Class类的getMethod(String name, Class...parameterTypes)方法获取一个Method对象，并设置此方法操作时所需要的的参数类型
   2. 调用Method对象的invoke(Object obj,Object[] args)方法，并向方法中传递目标obj对象的参数信息

##### 使用Java的反射机制，一般需要遵循三步：

1. 获得你想操作类的对象
2. 通过第一步获得的Class对象去取得操作类的方法或是属性名
3. 操作第二步取得的方法或是属性

##### 获取Class对象的常用三种方式

1. 调用Class的静态方法forName
2. 使用类的.class方法： Class cls = String.class
3. 调用对象的getClass方法

##### demo

```java
package com.chenHao.reflection;

import java.lang.reflect.Method;

/**
 * Java 反射练习。
 *
 * @author chenHao
 */
public class ReflectionTest {
    public static void main(String[] args) throws Exception {
        DisPlay disPlay = new DisPlay();
        // 获得Class
        Class<?> cls = disPlay.getClass();
        // 通过Class获得DisPlay类的show方法
        Method method = cls.getMethod("show", String.class);
        // 调用show方法
        method.invoke(disPlay, "chenHao");
    }
}

class DisPlay {
    public void show(String name) {
        System.out.println("Hello :" + name);
    }
}
```

##### 注意

getMethod方法的第一个参数是方法名，第二个是此方法的参数类型，如果是多个参数，接着添加参数就可以了，因为getMethod是可变参数方法。意invoke的第一个参数，是DisPlay类的一个对象，也就是调用DisPlay类哪个对象的show方法，第二个参数是给show方法传递的参数。类型和个数一定要与getMethod方法一直。

##### demo2

```java
 private static Object copyBean(Object from) throws Exception {
35         // 取得拷贝源对象的Class对象
36         Class<?> fromClass = from.getClass();
37         // 取得拷贝源对象的属性列表
38         Field[] fromFields = fromClass.getDeclaredFields();
39         // 取得拷贝目标对象的Class对象
40         Object ints = fromClass.newInstance();
41         for (Field fromField : fromFields) {
42             // 设置属性的可访问性
43             fromField.setAccessible(true);
44             // 将拷贝源对象的属性的值赋给拷贝目标对象相应的属性
45             fromField.set(ints, fromField.get(from));
46         }
47 
48         return ints;
49     }
50 }
```

总结:Field提供了get和set方法获取和设置属性的值，但是由于属性是私有类型，所以需要设置属性的可访问性为true，

第二种方法:AccessibleObject.setAccessible(fromFields, true);直接将所有字段设置为可访问的

#### 简 化版Mybatis工具

### Java泛型详解

##### 概述

泛型，参数化类型。泛型的本质是为了参数化类型（在不创建新的类型的情况下，通过泛型指定不同类型来控制具体限制的类型）。

#### 类型擦除

##### 泛型擦除只在编译阶段有效

```java
List<String> stringArrayList = new ArrayList<>();
List<Integer> integerArrayList = new ArrayList<> ();
Class classStringArrayList = stringArrayList.getClass();
Class classIntegerArrayList = integerArrayList.getClass();
if (classIntegerArrayList.equals(classStringArrayList)) {
	System.out.println("相同");
}

```

总结:在编译过程中，正确检验泛型结果后，会将泛型的相关信息擦出，并且在对象进入和离开方法的边界处添加类型检查和类型转换方法

泛型类型在逻辑上可以看成多个不同的类型，实际上都是相同的基本类型

##### 定义

类型擦除指的是通过类型参数合并，将泛型类型实例关联到同一份字节码上。编译器只为泛型类型生成一份字节码，将其实例关联到这份字节码上。类型擦除关键在于从泛型类型清楚类型参数的相关信息，并且再必要的时候添加类型检查和类型转换方法。

擦除主要过程:将所有的泛型参数用其最左边界（最顶级的父类）类型替换 ，移除所有类型参数

##### Java编译处理泛型的过程

code1

```java
interface Comparable<A> {
    public int compareTo(A that);
}

public final class NumericValue implements Comparable<NumericValue> {
    private byte value;

    public NumericValue(byte value) {
        this.value = value;
    }

    public byte getValue() {
        return value;
    }

    public int compareTo(NumericValue that) {
        return this.value - that.value;
    }
}
//反编译之后
//关键部分
public int compareTo(Object obj) {
    return compareTo((NumericValue) obj);
}
```

因为接口被移除参数，导致NumericValue没有实现接口。所以编译器做了一个桥接

#### 泛型的使用

##### 泛型类

泛型的类型参数只能是类类型，不能是简单类型

不能对确切的泛型类型使用instancof操作。if（ex_num instanceof Generic<Number>）{}

##### 泛型接口

code1

```java
public interface Generator<T> {
	public T next();
}
/**当实现泛型接口时，未传入泛型实参时,与泛型类的定义相同，在声明类的时候，需将泛型的声明也一起加到类中
否则会报错

*/
class FruitGenerator<T> implements Generator<T> {
    @Override
    public T next() {
        return null;
    }
}
/**当实现泛型接口时，传入泛型实参时，则所有使用泛型的地方都需要替换成传入的实参类型
*/
class FruitGenerator implements Generator<String> {
    private String[] fruits = new String[] {"Apple","Banana","Pear"};
    @Override
    public String next() {
        Random rand = new Random();
        return fruits[rand.nextInt(3)];
        }
}
```



##### 泛型通配符

类型通配符一般是使用?代替具体类型的实参。当具体类型不确定的时候，这个通配符就是？；当操作类型时，不需要使用类型的具体功能时，只使用Object类中的功能，那么可以用？来表未知类型

#### 泛型方法

##### 基本介绍

1. public <T>声明为泛型方法
2. 只有声明了<T>此时才可以在方法中使用泛型泛型类型<T>

##### 基本用法

```java
//编译器会提示"Unknown class "T",对编译器来说这个还没有声明，不知道如何编译
public void showKey(T genericObj) {
    
}
```

##### 类中的泛型方法

```java
public class GenericFruit {
    class Fruit{
        @Override
        public String toString() {
            return "fruit";
        }
    }

    class Apple extends Fruit{
        @Override
        public String toString() {
            return "apple";
        }
    }

    class Person{
        @Override
        public String toString() {
            return "Person";
        }
    }

    class GenerateTest<T>{
        public void show_1(T t){
            System.out.println(t.toString());
        }

        //在泛型类中声明了一个泛型方法，使用泛型E，这种泛型E可以为任意类型。可以类型与T相同，也可以不同。
        //由于泛型方法在声明的时候会声明泛型<E>，因此即使在泛型类中并未声明泛型，编译器也能够正确识别泛型方法中识别的泛型。
        public <E> void show_3(E t){
            System.out.println(t.toString());
        }

        //在泛型类中声明了一个泛型方法，使用泛型T，注意这个T是一种全新的类型，可以与泛型类中声明的T不是同一种类型。
        public <T> void show_2(T t){
            System.out.println(t.toString());
        }
    }

    public static void main(String[] args) {
        Apple apple = new Apple();
        Person person = new Person();

        GenerateTest<Fruit> generateTest = new GenerateTest<Fruit>();
        //apple是Fruit的子类，所以这里可以
        generateTest.show_1(apple);
        //编译器会报错，因为泛型类型实参指定的是Fruit，而传入的实参类是Person
        //generateTest.show_1(person);

        //使用这两个方法都可以成功
        generateTest.show_2(apple);
        generateTest.show_2(person);

        //使用这两个方法也都可以成功
        generateTest.show_3(apple);
        generateTest.show_3(person);
    }
}
```

##### 静态方法与泛型

类中静态方法使用泛型:静态方法无法访问类上定义的泛型；如果静态方法要使用泛型的话，必须将静态方法也定义成泛型方法

#### 泛型上下边界

对传入的泛型类型实参进行上下边界的限制

```java
public void showKeyValue(Generic<? extends Number> obj) {
    System.out.println("泛型测试")
}

```

泛型方法中添加上下边界限制

```java
public <T extends Number> T showKeyName(Generic<T> contains) {
}
```

### 详解内部类

#### 为什么要使用内部类

内部类最吸引人的原因是：每个内部类都能独立地继承在一个《接口的》实现，无论外围类是否已经继承了某个(接口的实现)，对于内部类都没有影响

##### 内部类的特性

1. 内部类可以用多个实例，每个实例都有自已的状态信息，并且与其他外围对象的信息相互独立
2. 单个外围类中，可以让多个内部类以不同的方式实现同一个接口，或者继承同一个类
3. 创建内部类对象的时刻并不依赖于外围类对象的创建。
4. 内部类并没有令人疑惑的"is -a"关系，它就是一个独立的实体
5. 内部类提供了更好的封装，除了外围类，其他类都不能访问

#### 内部类基础

创建了一个内部类的时候，产生了与外围类一种联系，依赖这种联系，它可以无限制地访问外围类的元素

```java
public class OuterClass {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public class InnerClass {
        public InnerClass() {
            name = "shencang";
            age = 21;

        }
        public void display() {
            System.out.println("name:" + getName() + "; age" + getAge());
        }
    }

    public static void main(String[] args) {
        OuterClass outerClass = new OuterClass();
        //创建内部类的方式
        OuterClass.InnerClass innerClass = outerClass.new InnerClass();
        innerClass.display();
    }
}

```

当创建某个外围类的内部对象时，此时内部类对象必定会捕获一个指向外围类对象的引用，只要访问外围类成员的时候，就会用这个引用选择外围类的成员 

生成外围类对象的引用，使用OuterClassName.this产生一个正确引用外部类的引用了。这是编译期间

```java
public class OuterClass {
    public void display() {
        System.out.println("OuterClass...")
    }
    public class InnerClass {
        public OuterClass getOuterClass() {
            return OuterClass.this;
        }
    }
}
```

内部类是编译时的概念，编译成功后就与外围类属于两个完全不同的类

#### 静态内部类

##### 静态内部类

因为static所以不依赖外围类对象实例而独立存在，静态内部类的可以访问外围类中的所有静态成员，包括private静态成员，但是不能使用任何外围类的非Static成员变量和方法

静态内部类是所有内部类独立性最高的内部类，在创建对象、继承（实现接口）、扩展子类等使用方式与外围类没有多大的区别

#### 成员内部类

##### 成员内部类

定义在类的内部，而且与成员方法、成员变量同级，也是外围类的成员之一，因此与外围类是紧密关联的

成员内部类的三个特点

1. 成员内部类可以访问外围类的所有成员，包括私有成员
2. 成员内部类是不可以声明静态成员的（包括静态变量、静态方法、静态成员类、嵌套接口），可以声明static final的变量，这是因为编译器对final类型的特殊 处理，是可以直接写入字节码
3. 成员内部类对象都隐式保存了一个引用，指向创建它的外部类对象；成员内部类的入口是由外围类对象保持着（静态内部类的入口，则直接由外围类保持着）

##### 成员内部类中的this、new关键字

1. 获取外部类对象：OuterClass.this
2. 明确指定使用外部类成员（外部类成员与成员内部类发生冲突）:OuterClass.this.成员名
3. 创建内部类对象的new:外围类对象.new

##### 补充

1. 成员内部类可以继承包含成员内部类，而且不管一个内部类被嵌套了多少层，它都能透明地访问它的所有外部类所有成员
2. 成员内部类可以继承嵌套多层的成员内部类，但无法嵌套静态内部类；静态内部类则都可以继续嵌套这两种内部类

##### 继承成员内部类

在内部类访问权限允许的情况下，成员内部类也是可以被继承的。但因为成员内部类的对象依赖于外围类的对象，或者说，成员内部类的构造器入口由外围类的对象把持着。因此继承了成员内部类的子类必须要与一个外围类对象关联起来。同时，子类的构造器是必须要调用父类的构造器方法，所以也只能通过父类的外围类对象来调用父类构造器

```java
public class ChildClass extends OuterClass.InnerClass{
    //成员内部类的子类的构造器的格式
    public ChildClass(OuterClass outerClass) {
        outerClass.super();//通过外围类的对象调用父类的构造方法
    }
}
```



#### 局部内部类

##### 局部内部类

在方法、构造器、初始化块中声明的类，在结构上类似于一个局部变量。因此局部内部类是不能使用访问修饰符

局部内部类的两个访问限制:

1. 对于局部变量，局部内部类只能访问final的局部变量。局部变量可不用final修饰，也可以被局部内部类访问，但你必须时刻记住此局部变量已经是final了，不能再改变
2. 对于类的全局成员，局部内部类定义在实例环境中（构造器、对象成员方法、实例初始化块），则可以访问外围类的所有成员；但如果内部类定义在静态环境中（静态初始化块、静态方法），则只能访问外围类的静态成员

#### 匿名内部类

##### 匿名内部类

与局部内部类很相似，只不过匿名内部类是一个没有给定名字的内部类，在创建这个匿名内部类后，便会立即用来创建并返回此内部类的一个对象引用

##### 作用

匿名内部类用于隐式继承某个类（重写里面的方法或实现抽象方法）或者实现某个接口

##### 匿名内部类的访问限制

同局部内部类

##### 匿名内部类的优缺点

优点：编码方便快捷

缺点：

1. 只能继承一个类或实现一个接口，不能再继承其他类或其他接口
2. 只能用于创建一次对象实例

##### demo

```java
class MyOuterClass {
    private int x = 5;
    void createThread() {
        final int a = 10;
        int b = 189;
        // 匿名内部类继承Thread类，并重写Run方法
        Thread thread = new Thread("thread-1") {
            int c = x;  //访问成员变量
            int d = a;  //final的局部变量
            int e = b; //访问没有用final修饰的局部变量
            @Override
            public void run() {
                System.out.println("这是线程thread-1");
            }
        };
        // 匿名内部类实现Runnable接口
        Runnable r = new Runnable() {
            @Override
            public void run() {
                System.out.println("线程运行中");
            }
        };
    }
}
```

### 详解匿名内部类

#### 使用匿名内部类内部类

1.  由于匿名内部类不能是抽象类，所以它必须要实现它的抽象父类或者接口里面所有的抽象方法
2. 对于匿名内部类的使用它是存在一个缺陷的，就是它仅能被使用一次，创建匿名内部类时它会立即创建一个该类的实例，该类的定义会立即消失，所以匿名内部类是不能够被重复使用

#### 注意事项

1. 使用匿名内部类时，我们必须是继承一个类或者实现一个接口，但是两者不可兼得，同时也只能继承一个类或者实现一个接口
2. 匿名内部类中是不能定义构造函数的
3. 匿名内部类中不能存在任何的静态成员变量和静态方法
4. 匿名内部类为局部内部类，所以局部内部类的所有限制同样对匿名内部类生效
5. 匿名内部类不能是抽象的，它必须要实现继承的类或者实现的接口的所有抽象方法

#### 使用的形参为何要final

==当所在的方法的形参需要被内部类里面使用时，该形参必须为final==

##### 为什么要final呢？

 首先我们知道在内部类编译成功后，它会产生一个class文件，该class文件与外部类并不是同一class文件，仅仅只保留对外部类的引用

分析

```java
//编译前
public class OuterClass {
    public void display(final String name,String age){
        class InnerClass{
            void display(){
                System.out.println(name);
            }
        }
    }
}
//编译后
public class OuterClass$InnerClass {
    public InnerClass(String name,String age){
        this.InnerClass$name = name;
        this.InnerClass$age = age;
    }
    
    
    public void display(){
        System.out.println(this.InnerClass$name + "----" + this.InnerClass$age );
    }
}
```

**，拷贝引用，为了避免引用值发生改变，例如被外部类的方法修改等，而导致内部类得到的值不一致，于是用final来让该引用不可改变**

  **故如果定义了一个匿名内部类，并且希望它使用一个其外部定义的参数，那么编译器会要求该参数引用是final的** 

### Java最全异常详解

#### 异常简介

##### 什么是异常

程序运行时，发生的不被期望的事件，它阻止了程序按照程序员的预期正常执行，这就是异常

##### Java异常的分类和类结构图

1.Java中的所有不正常类都继承于Throwable类。Throwable主要包括两个大类，一个是Error类，另一个是Exception类；

![](F:%5C%E6%A1%8C%E9%9D%A2%5CNotes%5C1168971-20190226100958279-424834144.png)

1. 错误：Error类以及他的子类的实例，代表了JVM本身的错误。包括**虚拟机错误**和**线程死锁**，一旦Error出现了，程序就彻底的挂了，被称为程序终结者；例如，JVM 内存溢出。一般地，程序不会从错误中恢复
2. Exception以及他的子类，代表程序运行时发生的各种不期望发生的事件。可以被Java异常处理机制使用，是异常处理的核心。Exception主要包括两大类，**非检查异常**（RuntimeException）和**检查异常**（其他的一些异常）![](F:%5C%E6%A1%8C%E9%9D%A2%5CNotes%5CJava%E5%9F%BA%E7%A1%80.assets%5C1168971-20190226101501136-281380556-1653364284744.png)
3. **非检查异常（unckecked exception）**：Error 和 RuntimeException 以及他们的子类。javac在编译时，不会提示和发现这样的异常，不要求在程序处理这些异常。所以如果愿意，我们可以编写代码处理（使用try…catch…finally）这样的异常，也可以不处理。对于这些异常，我们应该修正代码，而不是去通过异常处理器处理 。这样的异常发生的原因多半是代码写的有问题。如除0错误ArithmeticException，错误的强制类型转换错误ClassCastException，数组索引越界ArrayIndexOutOfBoundsException，使用了空对象NullPointerException等等
4. **检查异常（checked exception）**：除了Error 和 RuntimeException的其它异常。javac强制要求程序员为这样的异常做预备处理工作（使用try…catch…finally或者throws）。在方法中要么用try-catch语句捕获它并处理，要么用throws子句声明抛出它，否则编译不会通过。这样的异常一般是由程序的运行环境导致的。因为程序可能被运行在各种未知的环境下，而程序员无法干预用户如何使用他编写的程序，于是程序员就应该为这样的异常时刻准备着。如SQLException , IOException,ClassNotFoundException 等。

#### 捕获异常

##### 基础语法

1. try块：负责捕获异常，一旦try中发现异常，程序的控制权将被移交给catch块中的异常处理程序。try无法独立存在必须与catch或者finally块同存
2. catch块：如何处理？比如发出警告：提示、检查配置、网络连接，记录错误等。执行完catch块之后程序跳出catch块，继续执行后面的代码。**多个catch块处理的异常类，要按照先catch子类后catch父类的处理方式，因为会【就近处理】异常（由上自下）**
3. ）finally：最终执行的代码，用于关闭和释放资源。
4. 异常处理的任务就是将执行控制流从异常发生的地方转移到能够处理这种异常的地方去。也就是说：当一个函数的某条语句发生异常时，这条语句的后面的语句不会再执行，它失去了焦点。执行流跳转到最近的匹配的异常处理catch代码块去执行，异常被处理完后，执行流会接着在“处理了这个异常的catch代码块”后面接着执行

##### 多重捕获块

语法

```java
try {
    file = new FileInputStream(fileName);
    x = (byte) file.read();
} catch(FileNotFoundException f) { // Not valid!
    f.printStackTrace();
    return -1;
} catch(IOException i) {
    i.printStackTrace();
    return -1;
}
```

如果保护代码中发生异常，异常被抛给第一个 catch 块。

如果抛出异常的数据类型与 ExceptionType1 匹配，它在这里就会被捕获。

如果不匹配，它会被传递给第二个 catch 块。

如此，直到异常被捕获或者通过所有的 catch 块。

多重异常处理代码块顺序问题：**先子类再父类**（顺序不对编译器会提醒错误），finally语句块处理最终将要执行的代码

#### throw和throws关键字

##### throw异常抛出语句

hrow ----将产生的异常抛出，是抛出异常的一个**动作**。

如果不使用try catch语句去尝试捕获这种异常， 或者添加声明，将异常抛出给更上一层的调用者进行处理，则程序将会在这里停止，并不会执行剩下的代码。

一般会用于程序出现某种逻辑时程序员主动抛出某种特定类型的异常

语法格式:throw new xxx();

##### throws函数声明

throws----声明将要抛出何种类型的异常（**声明**）

当某个方法可能会抛出某种异常时用于throws 声明可能抛出的异常，然后交给上层调用它的方法程序处理

demo

```java
public static void function() throws NumberFormatException{ 
    String s = "abc"; 
    System.out.println(Double.parseDouble(s)); 
  } 
    
  public static void main(String[] args) { 
    try { 
      function(); 
    } catch (NumberFormatException e) { 
      System.err.println("非数据类型不能转换。"); 
      //e.printStackTrace(); 
    } 
}
//哪个方法调用，则交给调用的那个方法处理
```



##### throw和throws的比较

1. throws出现在方法函数头；而throw出现在函数体
2. throws表示出现异常的一种可能性，并不一定会发生这些异常；throw则是抛出了异常，执行throw则一定抛出了某种异常对象
3. 两者都是消极处理异常的方式（这里的消极并不是说这种方式不好），只是抛出或者可能抛出异常，但是不会由函数去处理异常，真正的处理异常由函数的上层调用处理

demo

```java
void doA(int a) throws (Exception1,Exception2,Exception3){
      try{
         ......
 
      }catch(Exception1 e){
       throw e;
      }catch(Exception2 e){
       System.out.println("出错了！");
      }
      if(a!=b)
       throw new Exception3("自定义异常");
}
```

1.代码块中可能会产生3个异常，(Exception1,Exception2,Exception3)。
2.如果产生Exception1异常，则捕获之后再抛出，由该方法的调用者去处理。
3.如果产生Exception2异常，则该方法自己处理了（即System.out.println("出错了！");）。所以该方法就不会再向外抛出Exception2异常了，void doA() throws Exception1,Exception3 里面的**Exception2也就不用写了。因为已经用try-catch语句捕获并处理了。**
4.Exception3异常是该方法的某段逻辑出错，程序员自己做了处理，在该段逻辑错误的情况下抛出异常Exception3，则该方法的调用者也要处理此异常。这里用到了自定义异常，该异常下面会由解释。

**注意：**如果某个方法调用了抛出异常的方法，那么必须添加try catch语句去尝试捕获这种异常， 或者添加声明，将异常抛出给更上一层的调用者进行处理

#### 自定义异常 

##### 为什么要使用自定义异常，有什么好处？

1. 我们在工作的时候，项目是分模块或者分功能开发的 ,基本不会你一个人开发一整个项目，使用自定义异常类就**统一了对外异常展示的方式**
2. 有时候我们遇到某些校验或者问题时，**需要直接结束掉当前的请求**，这时便可以通过抛出自定义异常来结束，如果你项目中使用了SpringMVC比较新的版本的话有控制器增强，可以通过@ControllerAdvice注解写一个控制器增强类来拦截自定义的异常并响应给前端相应的信息
3. 自定义异常可以在我们项目中某些**特殊的业务逻辑**时抛出异常，比如"中性".equals(sex)，性别等于中性时我们要抛出异常，而Java是不会有这种异常的。系统中有些错误是符合Java语法的，但不符合我们项目的业务逻辑

##### 怎么使用自定义异常？

1. 所以异常都必须是throwable的子类
2. 写一个检查性异常，需要继承Exceptin类
3. 运行时异常，需要继承RuntimeException类

自定义异常

```java
package com.hysum.test;

public class MyException extends Exception {
     /**
     * 错误编码
     */
    private String errorCode;

    public MyException(){}
    
    /**
     * 构造一个基本异常.
     *
     * @param message
     *        信息描述
     */
    public MyException(String message){
        super(message);
    }

    public String getErrorCode() {
        return errorCode;
    }

    public void setErrorCode(String errorCode) {
        this.errorCode = errorCode;
    }
}
```

#### finally块和return

demo1

```java
public static void main(String[] args)
{
    int re = bar();
    System.out.println(re);
}
private static int bar() 
{
    try{
        return 5;
    } finally{
        System.out.println("finally");
    }
}
/*输出：
finally
5
*/
```

：try…catch…finally中的return 只要能执行，就都执行了，他们共同向同一个内存地址（假设地址是0×80）写入返回值，后执行的将覆盖先执行的数据，而真正被调用者取的返回值就是最后一次写入的

##### finally中的return会覆盖try或者catch中的返回值

```java
public static void main(String[] args){
    int result;

    result  =  foo();
    System.out.println(result);     /////////2

    result = bar();
    System.out.println(result);    /////////2
}

@SuppressWarnings("finally")
public static int foo(){
    trz{
        int a = 5 / 0;
    } catch (Exception e){
        return 1;
    } finally{
        return 2;
    }

}

@SuppressWarnings("finally")
public static int bar(){
    try {
        return 1;
    }finally {
        return 2;
    }
}

```

**finally中的return会抑制（消灭）前面try或者catch块中的异常**

```java
class TestException{
    public static void main(String[] args){
        int result;
        try{
            result = foo();
            System.out.println(result);           //输出100
        } catch (Exception e){
            System.out.println(e.getMessage());    //没有捕获到异常
        }
 
        try{
            result  = bar();
            System.out.println(result);           //输出100
        } catch (Exception e){
            System.out.println(e.getMessage());    //没有捕获到异常
        }
    }
 
    //catch中的异常被抑制
    @SuppressWarnings("finally")
    public static int foo() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }catch(ArithmeticException amExp) {
            throw new Exception("我将被忽略，因为下面的finally中使用了return");
        }finally {
            return 100;
        }
    }
 
    //try中的异常被抑制
    @SuppressWarnings("finally")
    public static int bar() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }finally {
            return 100;
        }
    }
}
```

**finally中的return会抑制（消灭）前面try或者catch块中的异常**

```java
class TestException{
    public static void main(String[] args){
        int result;
        try{
            result = foo();
            System.out.println(result);           //输出100
        } catch (Exception e){
            System.out.println(e.getMessage());    //没有捕获到异常
        }
 
        try{
            result  = bar();
            System.out.println(result);           //输出100
        } catch (Exception e){
            System.out.println(e.getMessage());    //没有捕获到异常
        }
    }
 
    //catch中的异常被抑制
    @SuppressWarnings("finally")
    public static int foo() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }catch(ArithmeticException amExp) {
            throw new Exception("我将被忽略，因为下面的finally中使用了return");
        }finally {
            return 100;
        }
    }
 
    //try中的异常被抑制
    @SuppressWarnings("finally")
    public static int bar() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }finally {
            return 100;
        }
    }
}
```

**finally中的异常会覆盖（消灭）前面try或者catch中的异常**

```java
class TestException{
    public static void main(String[] args){
        int result;
        try{
            result = foo();
        } catch (Exception e){
            System.out.println(e.getMessage());    //输出：我是finaly中的Exception
        }
 
        try{
            result  = bar();
        } catch (Exception e){
            System.out.println(e.getMessage());    //输出：我是finaly中的Exception
        }
    }
 
    //catch中的异常被抑制
    @SuppressWarnings("finally")
    public static int foo() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }catch(ArithmeticException amExp) {
            throw new Exception("我将被忽略，因为下面的finally中抛出了新的异常");
        }finally {
            throw new Exception("我是finaly中的Exception");
        }
    }
 
    //try中的异常被抑制
    @SuppressWarnings("finally")
    public static int bar() throws Exception{
        try {
            int a = 5/0;
            return 1;
        }finally {
            throw new Exception("我是finaly中的Exception");
        }
    }
}
```

**建议**

1. 不要在finally中使用return
2. 不要在finallyz中抛出异常
3. 减轻finally的任务，不要在finally中做一些其它的事情，finally块仅仅用来释放资源是最合适的
4. 将尽量将所有的return写在函数的最后面，而不是try … catch … finally中

#### 使用加强controller做全局异常处理

**@ExceptionHandler注解**

```java
/** Created by ChenHao.
 * 自定义异常
 */
public class SystemException extends RuntimeException{
    private String code;//状态码
    public SystemException(String message, String code) {
        super(message);
        this.code = code;
    }
    public String getCode() {
        return code;
    }
}
```

所谓加强Controller就是@ControllerAdvice注解，有这个注解的类中的方法的某些注解会应用到所有的Controller里，其中就包括@ExceptionHandler注解

```java
/**
 * Created by ChenHao on 2019/02/26.
 * 全局异常处理，捕获所有Controller中抛出的异常。
 */
@ControllerAdvice
public class GlobalExceptionHandler {
   //处理自定义的异常
   @ExceptionHandler(SystemException.class) 
   @ResponseBody
   @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
   public Object customHandler(SystemException e){
      e.printStackTrace();
      return WebResult.buildResult().status(e.getCode()).msg(e.getMessage());
   }
   //其他未处理的异常
   @ExceptionHandler(Exception.class)
   @ResponseBody
   @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
   public Object exceptionHandler(Exception e){
      e.printStackTrace();
      return WebResult.buildResult().status(Config.FAIL).msg("系统错误");
   }
}
```

登录逻辑

```java
/**
 * Created by ChenHao on 2016/12/28.
 * 账号
 */
@RestController
@RequestMapping("passport")
public class PassportController {
    PassportService passportService;
        @RequestMapping("login")
    public Object doLogin(HttpSession session, String username, String password){
        User user = passportService.doLogin(username, password);
        session.setAttribute("user", user);
        return WebResult.buildResult().redirectUrl("/student/index");
    }
}
```

而在passprotService的doLogin方法中，可能会抛出用户名或密码错误等异常，然后就会交由GlobalExceptionHandler去处理，直接返回异常信息给前端，然后前端也不需要关心是否返回了异常，因为这些都已经定义好了

一个异常在其中流转的过程为

比如doLogin方法抛出了自定义异常，其code为：FAIL，message为：用户名或密码错误，由于在controller的方法中没有捕获这个异常，所以会将异常抛给GlobalExceptionHandler，然后GlobalExceptionHandler通过WebResult将状态码和提示信息返回给前端，前端通过默认的处理函数，弹框提示用户“用户名或密码错误”。而对于这样的一次交互，我们根本不用编写异常处理部分的逻辑

### equals()与hashcode()方法详解

#### 概述

Object类是类继承结构的基础，所以是每一个类的父类。所有的对象，包括数组，都实现了在Object类中定义的方法

#### equals方法详解

`equals()`方法是用来判断其他的对象是否和该对象相等

equals()方法在object类中定义如下

```java
public boolean equals(Object obj) {  
    return (this == obj);  
}  
```

很明显是对两个对象的地址值进行的比较（即比较引用是否相同）。但是我们知道，**String 、Math、Integer、Double等这些封装类在使用equals()方法时，已经覆盖了object类的equals()方法**

string类下

```java
public boolean equals(Object anObject) {  
    if (this == anObject) {  
        return true;  
    }  
    if (anObject instanceof String) {  
        String anotherString = (String)anObject;  
        int n = count;  
        if (n == anotherString.count) {  
            char v1[] = value;  
            char v2[] = anotherString.value;  
            int i = offset;  
            int j = anotherString.offset;  
            while (n– != 0) {  
                if (v1[i++] != v2[j++])  
                    return false;  
            }  
            return true;  
        }  
    }  
    return false;  
}
```

需要注意的是当equals()方法被override时，hashCode()也要被override。按照一般hashCode()方法的实现来说，相等的对象，它们的hash code一定相等

#### hashcode方法详解

`hashCode()`方法给对象返回一个hash code值。这个方法被用于hash tables，例如HashMap

##### 性质

1. 在一个Java应用的执行期间，如果一个对象提供给equals做比较的信息没有被修改的话，该对象多次调用`hashCode()`方法，该方法必须始终如一返回同一个integer
2. 如果两个对象根据equals(Object)方法是相等的，那么调用二者各自的`hashCode()`方法必须产生同一个integer结果
3. 并不要求根据`equals(java.lang.Object)`方法不相等的两个对象，调用二者各自的hashCode()方法必须产生不同的integer结果。然而，程序员应该意识到对于不同的对象产生不同的integer结果，有可能会提高hash table的性能
4. 大量的实践表明，由`Object`类定义的`hashCode()`方法对于不同的对象返回不同的integer

在object类中，hashCode定义如下

```java
public native int hashCode();
```

说明是一个本地方法，它的实现是根据本地机器相关的。当然我们可以在自己写的类中覆盖hashcode()方法，比如String、Integer、Double等这些类都是覆盖了hashcode()方法的。例如在String类中定义的hashcode()方法如下:

```java
public int hashCode() {  
    int h = hash;  
    if (h == 0) {  
        int off = offset;  
        char val[] = value;  
        int len = count;  
        for (int i = 0; i < len; i++) {  
            h = 31 * h + val[off++];  
        }  
        hash = h;  
    }  
    return h;  
}
```

想要弄明白hashCode的作用，必须要先知道Java中的集合。　　
总的来说，Java中的集合（Collection）有两类，一类是List，再有一类是Set。前者集合内的元素是有序的，元素可以重复；后者元素无序，但元素不可重复。这里就引出一个问题：要想保证元素不重复，可两个元素是否重复应该依据什么来判断呢？这就是Object.equals方法了。但是，如果每增加一个元素就检查一次，那么当元素很多时，后添加到集合中的元素比较的次数就非常多了。也就是说，如果集合中现在已经有1000个元素，那么第1001个元素加入集合时，它就要调用1000次equals方法。这显然会大大降低效率。 

哈希算法也称为散列算法，是将数据依特定算法直接指定到一个地址上，初学者可以简单理解，hashCode方法实际上返回的就是对象存储的物理地址（实际可能并不是）

这样一来，当集合要添加新的元素时，先调用这个元素的hashCode方法，就一下子能定位到它应该放置的物理位置上。如果这个位置上没有元素，它就可以直接存储在这个位置上，不用再进行任何比较了；如果这个位置上已经有元素了，就调用它的equals方法与新元素进行比较，相同的话就不存了，不相同就散列其它的地址。所以这里存在一个冲突解决的问题。这样一来实际调用equals方法的次数就大大降低了，几乎只需要一两次

**简而言之，在集合查找时，hashcode能大大降低对象比较次数，提高查找效率！**

Java对象的eqauls方法和hashCode方法是这样规定的：

1. **相等（相同）的对象必须具有相等的哈希码（或者散列码）**
2. **如果两个对象的hashCode相同，它们并不一定相同**

#### 关于第一点，相等（相同）的对象必须具有相等的哈希码（或者散列码），为什么？

想象一下，假如两个Java对象A和B，A和B相等（eqauls结果为true），但A和B的哈希码不同，则A和B存入HashMap时的哈希码计算得到的HashMap内部数组位置索引可能不同，那么A和B很有可能允许同时存入HashMap，显然相等/相同的元素是不允许同时存入HashMap，HashMap不允许存放重复元素

#### 关于第二点，两个对象的hashCode相同，它们并不一定相同

不同对象的hashCode可能相同；假如两个Java对象A和B，A和B不相等（eqauls结果为false），但A和B的哈希码相等，将A和B都存入HashMap时会发生哈希冲突，也就是A和B存放在HashMap内部数组的位置索引相同这时HashMap会在该位置建立一个链接表，将A和B串起来放在该位置，显然，该情况不违反HashMap的使用原则，是允许的。当然，哈希冲突越少越好，尽量采用好的哈希算法以避免哈希冲突

Java对于eqauls方法和hashCode方法是这样规定的：

1. .如果两个对象相同，那么它们的hashCode值一定要相同
2. 如果两个对象的hashCode相同，它们并不一定相同（这里说的对象相同指的是用eqauls方法比较）
3. .equals()相等的两个对象，hashcode()一定相等；equals()不相等的两个对象，却并不能证明他们的hashcode()不相等.换句话说，equals()方法不相等的两个对象，hashcode()有可能相等（我的理解是由于哈希码在生成的时候产生冲突造成的）。反过来，hashcode()不等，一定能推出equals()也不等；hashcode()相等，equals()可能相等，也可能不等

在object类中，hashcode()方法是本地方法，返回的是对象的地址值，而object类中的equals()方法比较的也是两个对象的地址值，如果equals()相等，说明两个对象地址值也相等，当然hashcode()也就相等了；**在String类中，equals()返回的是两个对象内容的比较**，当两个对象内容相等时，Hashcode()方法根据String类的重写代码的分析，也可知道hashcode()返回结果也会相等。以此类推，可以知道Integer、Double等封装类中经过重写的equals()和hashcode()方法也同样适合于这个原则。当然没有经过重写的类，在继承了object类的equals()和hashcode()方法后，也会遵守这个原则

#### Hashset、Hashmap、Hashtable与hashcode()和equals()的密切关系

在hashset中不允许出现重复对象，元素的位置也是不确定的。在hashset中又是怎样判定元素是否重复的呢？在java的集合中，判断两个对象是否相等的规则是：

1. .判断两个对象的hashCode是否相等
   1. 如果不相等，认为两个对象也不相等，完毕
      如果相等，转入2
         （这一点只是为了提高存储效率而要求的，其实理论上没有也可以，但如果没有，实际使用时效率会大大降低，所以我们这里将其做为必需的。）
2. .判断两个对象用equals运算是否相等
   1.   如果不相等，认为两个对象也不相等
          如果相等，认为两个对象相等（equals()是判断两个对象是否相等的关键）

demo

```java
package com.bijian.study;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
public class HashSetTest {
    public static void main(String args[]) {
        String s1 = new String("aaa");
        String s2 = new String("aaa");
        System.out.println(s1 == s2);
        System.out.println(s1.equals(s2));
        System.out.println(s1.hashCode());
        System.out.println(s2.hashCode());
        Set hashset = new HashSet();
        hashset.add(s1);
        hashset.add(s2);
        Iterator it = hashset.iterator();
        while (it.hasNext()) {
            System.out.println(it.next());
        }
    }
}

运行结果：
false
true
96321
96321
aaa
```

这是因为String类已经重写了equals()方法和hashcode()方法，所以hashset认为它们是相等的对象，进行了重复添加。

demo2

```java
package com.bijian.study;
import java.util.HashSet;
import java.util.Iterator;
public class HashSetTest {
    public static void main(String[] args) {
        HashSet hs = new HashSet();
        hs.add(new Student(1, "zhangsan"));
        hs.add(new Student(2, "lisi"));
        hs.add(new Student(3, "wangwu"));
        hs.add(new Student(1, "zhangsan"));
        Iterator it = hs.iterator();
        while (it.hasNext()) {
            System.out.println(it.next());
        }
    }
}
class Student {
    int num;
    String name;
    Student(int num, String name) {
        this.num = num;
        this.name = name;
    }
    public String toString() {
        return num + ":" + name;
    }
}
运行结果：
1:zhangsan  
3:wangwu  
2:lisi  
1:zhangsan
```

为什么会生成不同的哈希码值呢？上面我们在比较s1和s2的时候不是生成了同样的哈希码吗？原因就在于我们自己写的Student类并没有重新自己的hashcode()和equals()方法，所以在比较时，是继承的object类中的hashcode()方法，而object类中的hashcode()方法是一个本地方法，比较的是对象的地址（引用地址），使用new方法创建对象，两次生成的当然是不同的对象了，造成的结果就是两个对象的hashcode()返回的值不一样，所以Hashset会把它们当作不同的对象对待

### 深拷贝和浅拷贝

#### 浅拷贝

万类之王Object。它有11个方法，有两个protected的方法，其中一个为clone方法。

该方法的签名是：

protected native Object clone() throws CloneNotSupportedException;

因为每个类直接或间接的父类都是Object，因此它们都含有clone()方法，但是因为该方法是protected，所以都不能在类外进行访问。

##### 步骤

1. 被复制的类需要实现Clonenable接口（不实现的话在调用clone方法会抛出CloneNotSupportedException异常) 该接口为标记接口(不含任何方法)
2. 覆盖clone()方法，访问修饰符设为public。方法中调用super.clone()方法得到需要的复制对象，（native为本地方法)

改造

```java
class Student implements Cloneable{
    private int number;
 
    public int getNumber() {
        return number;
    }
 
    public void setNumber(int number) {
        this.number = number;
    }
    
    @Override
    public Object clone() {
        Student stu = null;
        try{
            stu = (Student)super.clone();
        }catch(CloneNotSupportedException e) {
            e.printStackTrace();
        }
        return stu;
    }
}
public class Test {
    
    public static void main(String args[]) {
        
        Student stu1 = new Student();
        stu1.setNumber(12345);
        Student stu2 = (Student)stu1.clone();
        
        System.out.println("学生1:" + stu1.getNumber());
        System.out.println("学生2:" + stu2.getNumber());
        
        stu2.setNumber(54321);
    
        System.out.println("学生1:" + stu1.getNumber());
        System.out.println("学生2:" + stu2.getNumber());
    }
}
```

#### 深度复制

原因是浅复制只是复制了addr变量的引用，并没有真正的开辟另一块空间，将值复制后再将引用返回给新对象

```java
@Override
    public Object clone() {
        Student stu = null;
        try{
            stu = (Student)super.clone();
        }catch(CloneNotSupportedException e) {
            e.printStackTrace();
        }
        stu.addr = (Address)addr.clone();
        return stu;
    }
```

实现逻辑是在浅复制内，将成员变量类再浅拷贝到成员变量

### Java动态代理原理源码解析

####  静态代理

##### 静态代理

静态代理：由程序员创建或特定工具自动生成源代码，也就是在编译时就已经将接口，被代理类，代理类等确定下来。在程序运行之前，代理类的.class文件就已经生成

##### 静态代理实现简单实现

 代理模式最主要的就是有一个公共接口（Person），一个具体的类（Student），一个代理类（StudentsProxy）,代理类持有具体类的实例，代为执行具体类实例方法

代理模式就是在访问实际对象时引入一定程度的间接性，因为这种间接性，可以附加多种用途。这里的间接性就是指不直接调用实际对象的方法，那么我们在代理过程中就可以加上一些其他用途

##### 模式缺点

优点

1. 代理模式能够协调调用者和被调用者，在一定程度上降低了系统的耦合度
2.  代理对象可以在客户端和目标对象之间起到中介的作用，这样起到了的作用和保护了目标对象的

缺点

1. 由于在客户端和真实主题之间增加了代理对象，因此有些类型的代理模式可能会造成请求的处理速度变慢
2. 实现代理模式需要额外的工作，有些代理模式的实现非常复杂

#### 动态代理

##### 动态代理

代理类在程序运行时创建的代理方式被成为动态代理。而动态代理，代理类并不是在Java代码中定义的，而是在运行时根据我们在Java代码中的“指示”动态生成的

##### 动态代理简单实现

#### 动态代理原理分析

动态代理的优势在于可以很方便的对代理类的函数进行统一的处理，而不用修改每个代理类中的方法。是因为所有被代理执行的方法，都是通过在InvocationHandler中的invoke方法调用的，所以我们只要在invoke方法中统一处理，就可以对所有被代理的方法进行相同的操作了。

在JDK动态代理中涉及如下角色：

业务接口Interface、业务实现类target、业务处理类Handler、JVM在内存中生成的动态代理类$Proxy0

动态代理原理图：

![](F:%5C%E6%A1%8C%E9%9D%A2%5CNotes%5CJava%E5%9F%BA%E7%A1%80.assets%5C1168971-20190402172206471-456178976.png)

动态代理的过程是这样的：

1. Proxy通过传递给它的参数（interfaces/invocationHandler）生成代理类$Proxy0；
2. Proxy通过传递给它的参数（ClassLoader）来加载生成的代理类$Proxy0的字节码文件；

Proxy.newProxyInstance源码

```java
public static Object newProxyInstance(ClassLoader loader, Class<?>[] interfaces, InvocationHandler h) throws IllegalArgumentException {
　　// handler不能为空
    if (h == null) {
        throw new NullPointerException();
    }

    final Class<?>[] intfs = interfaces.clone();
    final SecurityManager sm = System.getSecurityManager();
    if (sm != null) {
        checkProxyAccess(Reflection.getCallerClass(), loader, intfs);
    }

    /*
     * Look up or generate the designated proxy class.
     */
　　// 通过loader和接口，得到代理的Class对象
    Class<?> cl = getProxyClass0(loader, intfs);

    /*
     * Invoke its constructor with the designated invocation handler.
     */
    try {
        final Constructor<?> cons = cl.getConstructor(constructorParams);
        final InvocationHandler ih = h;
        if (sm != null && ProxyAccessHelper.needsNewInstanceCheck(cl)) {
            // create proxy instance with doPrivilege as the proxy class may
            // implement non-public interfaces that requires a special permission
            return AccessController.doPrivileged(new PrivilegedAction<Object>() {
                public Object run() {
                    return newInstance(cons, ih);
                }
            });
        } else {
　　　　　　　// 创建代理对象的实例
            return newInstance(cons, ih);
        }
    } catch (NoSuchMethodException e) {
        throw new InternalError(e.toString());
    }
}
```

newInstance方法的源代码：

```java
private static Object newInstance(Constructor<?> cons, InvocationHandler h) {
    try {
        return cons.newInstance(new Object[] {h} );
    } catch (IllegalAccessException | InstantiationException e) {
        throw new InternalError(e.toString());
    } catch (InvocationTargetException e) {
        Throwable t = e.getCause();
        if (t instanceof RuntimeException) {
            throw (RuntimeException) t;
        } else {
            throw new InternalError(t.toString());
        }
    }
}
```

代理类工具

```java
/**
 * 代理类的生成工具 
 * @author ChenHao
 * @since 2019-4-2 
 */
public class ProxyGeneratorUtils {

    /**
     * 把代理类的字节码写到硬盘上 
     * @param path 保存路径 
     */
    public static void writeProxyClassToHardDisk(String path) {
        // 第一种方法
        // System.getProperties().put("sun.misc.ProxyGenerator.saveGeneratedFiles", true);  

        // 第二种方法  

        // 获取代理类的字节码  
        byte[] classFile = ProxyGenerator.generateProxyClass("$Proxy11", UserServiceImpl.class.getInterfaces());

        FileOutputStream out = null;

        try {
            out = new FileOutputStream(path);
            out.write(classFile);
            out.flush();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                out.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    public static void main(String[] args) {
        ProxyGeneratorUtils.writeProxyClassToHardDisk("C:/x/$Proxy11.class");
    }

}
```

反编译结果

```java
package org.fenixsoft.bytecode;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.lang.reflect.UndeclaredThrowableException;

public final class $Proxy0 extends Proxy
  implements DynamicProxyTest.IHello
{
  private static Method m3;
  private static Method m1;
  private static Method m0;
  private static Method m2;
  /**
  *注意这里是生成代理类的构造方法，方法参数为InvocationHandler类型，看到这，是不是就有点明白
  *super(paramInvocationHandler)，是调用父类Proxy的构造方法。
  *父类持有：protected InvocationHandler h;
  *Proxy构造方法：
  *    protected Proxy(InvocationHandler h) {
  *         Objects.requireNonNull(h);
  *         this.h = h;
  *     }
  *
  */
  public $Proxy0(InvocationHandler paramInvocationHandler)
    throws 
  {
    super(paramInvocationHandler);
  }
  
  /**
  * 
  *这里调用代理对象的sayHello方法，直接就调用了InvocationHandler中的invoke方法，并把m3传了进去。
  *this.h.invoke(this, m3, null);  this.h就是父类Proxy中保存的InvocationHandler实例变量
  *来，再想想，代理对象持有一个InvocationHandler对象，InvocationHandler对象持有一个被代理的对象，
  *再联系到InvacationHandler中的invoke方法。嗯，就是这样。
  */
  public final void sayHello()
    throws 
  {
    try
    {
      this.h.invoke(this, m3, null);
      return;
    }
    catch (RuntimeException localRuntimeException)
    {
      throw localRuntimeException;
    }
    catch (Throwable localThrowable)
    {
      throw new UndeclaredThrowableException(localThrowable);
    }
  }

  // 此处由于版面原因，省略equals()、hashCode()、toString()三个方法的代码
  // 这3个方法的内容与sayHello()非常相似。

  static
  {
    try
    {
      m3 = Class.forName("org.fenixsoft.bytecode.DynamicProxyTest$IHello").getMethod("sayHello", new Class[0]);
      m1 = Class.forName("java.lang.Object").getMethod("equals", new Class[] { Class.forName("java.lang.Object") });
      m0 = Class.forName("java.lang.Object").getMethod("hashCode", new Class[0]);
      m2 = Class.forName("java.lang.Object").getMethod("toString", new Class[0]);
      return;
    }
    catch (NoSuchMethodException localNoSuchMethodException)
    {
      throw new NoSuchMethodError(localNoSuchMethodException.getMessage());
    }
    catch (ClassNotFoundException localClassNotFoundException)
    {
      throw new NoClassDefFoundError(localClassNotFoundException.getMessage());
    }
  }
}
```

**java.lang.reflect.Proxy**

```java
public class Proxy implements java.io.Serializable {

    protected InvocationHandler h;

    private Proxy() {
    }

    protected Proxy(InvocationHandler h) {
        doNewInstanceCheck();
        this.h = h;
    }
    //略
}
```

这个代理类的实现代码也很简单,它为传入接口中的每一个方法,以及从 java.lang.Object中继承来的equals()、hashCode()、toString()方法都生成了对应的实现 ,并且统一调用了InvocationHandler对象的invoke()方法(代码中的“this.h”就是父类Proxy中保存的InvocationHandler实例变量)来实现这些方法的内容,各个方法的区别不过是传入的参数和Method对象有所不同而已,所以无论调用动态代理的哪一个方法,实际上都是在执行InvocationHandler.invoke()中的代理逻辑。

#### 缺点

**由Proxy创建的动态代理 不支持 对 实现类的代理**

动态代理类都 extend Proxy类，implements了代理的interface。
由于java不能多继承，这里已经继承了Proxy类了，不能再继承其他的类.
所以JDK的动态代理不支持对实现类的代理，只支持接口的代理

### 深入理解Java注解类型

#### 注解的概念

##### 注解的使用范围

1. 定义注解
2. 配置注解--把标记打在需要用到的程序代码上
3. 解析注解--在编译时或运行时检测到标记，并进行操作。

##### 基本语法

注解类型声明部分:注解在Java中，与类、接口、枚举类似。在底层实现上，所有定义的注解都会自动继承Java.lang.annotation.Annotation接口

定义的注解

1. 修饰符为public
2. 元素的类型只能是基本类型、String、Class、枚举类型、注解类型
3. 该元素的名称一般定义为名词，如果注解中只有一个元素，请把名字起为value
4. 该元素的名称一般定义为名词，如果注解中只有一个元素，请把名字起为value
5. default代表默认值，值必须和第2点定义的类型一致；`int age default 18`
6. 如果没有默认值，代表后续使用注解时必须给该类型元素赋值

##### 常用的元注解

#### @Target

```java
//@CherryAnnotation被限定只能使用在类、接口或方法上面
@Target(value = {ElementType.TYPE,ElementType.METHOD})
public @interface CherryAnnotation {
    String name();
    int age() default 18;
    int[] array();
}
```

#### @Retention

1. 如果一个注解被定义为RetentionPolicy.SOURCE，则它将被限定在Java源文件中，那么这个注解即不会参与编译也不会在运行期起任何作用，这个注解就和一个注释是一样的效果，只能被阅读Java文件的人看到；
2. 如果一个注解被定义为RetentionPolicy.CLASS，则它将被编译到Class文件中，那么编译器可以在编译时根据注解做一些处理动作，但是运行时JVM（Java虚拟机）会忽略它，我们在运行期也不能读取到；
3. 如果一个注解被定义为RetentionPolicy.RUNTIME，那么这个注解可以在运行期的加载阶段被加载到Class对象中。那么在程序运行阶段，我们可以通过反射得到这个注解，并通过判断是否有这个注解或这个注解中属性的值，从而执行不同的程序代码段。**我们实际开发中的自定义注解几乎都是使用的RetentionPolicy.RUNTIME；**









