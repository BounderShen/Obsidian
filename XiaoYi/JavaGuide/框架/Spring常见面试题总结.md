### Spring包含的模块有哪些
#### Core Contianer
1. core: Spring框架基本的核心工具类
2. beans：提供对bean的创建、配置和管理功能的支持
3. context：提供对国际化、事件传播、资源加载等功能的支持
4. expression：提供对表达式语言SpEL的支持，只依赖于core模块
#### AOP
1. aspects:该模块为AspectJ的集成提供支持
2. aop：面向切面编程的实现
#### Data Access
1. jdbc：提供了对数据库访问的抽象JDBC
2. tx：提供对事务的支持
3. orm: 提供一个对Hibernate、JPA、iBatis等ORM框架的支持
4. oxm：提供一个抽象层支撑
5. jxs：消息服务
#### Web
1. 对Web功能的实现提供一些最基础的支持
2. webMvc：提供对Spring Mvc的实现
3. webSocket：提供了对WebSocket，可以实现双端进行双向通信
4. Webflux: 提供了webflux的支持。响应式框架，不需要servlet，完全是一步的
#### Spring、Spring Mvc、Spring Boot
1. Spring: 包含多个功能模块，重要的是core模块（包含了对IOC依赖注入功能的支持）模块，其他模块都依赖于此模块
### Spring IOC
#### 谈谈对Spring IOC的了解
1. 是一种设计思想，将原本在程序中手动创建对象的控制权交给Spring 框架来管理
2. 控制：对象创建（实例化。管理）的权利
3. 反转：控制权交给外部环境（Spring 框架、IOC）
4. IOC实际上就是Map存放各种对象
#### 什么是Spring Bean
1. IOC管理的对象
2. 通过元数据定义可以让IOC帮我们管理哪个对象，xml文件、Java配置类、注解
#### 将一个类声明为Bean
1. Component、Service、Repository、Controler
#### @Component和@Bean的区别是什么
1. 一个用于类，一个用于方法
2. 通常是通过类路径扫描来自动侦测以及自动装配到 Spring 容器中（我们可以使用 `@ComponentScan` 注解定义要扫描的路径从中找出标识了需要装配的类自动装配到 Spring 的 bean 容器中）。`@Bean` 注解通常是我们在标有该注解的方法中定义产生这个 bean,`@Bean`告诉了 Spring 这是某个类的实例，当我需要用它的时候还给我
3. `@Bean` 注解比 `@Component` 注解的自定义性更强，而且很多地方我们只能通过 `@Bean` 注解来注册 bean
#### 注入Bean的注解有哪些
1. @Autowired和@Resource和@Inject
#### @Autowired和@Resource
1. Autowired：默认的注入方式为ByType根据类型匹配，优先根据接口类型去匹配并注入
2. 存在多个实现类时，转变为byName进行匹配
3. @Qualifier：指定名称
4. @Resource：byName->byType的转变；可以通过name来显示指定名称
#### Bean的作用域有哪些
1. singleton：IOC容器中只有唯一的bean实例。默认时单例
2. prototype：每次获取都是新的实例
3. request：(web应用可用)，每次请求产生一个新的Bean，尽在当前请求中
4. session：仅 Web 应用可用） : 每一次来自新 session 的 HTTP 请求都会产生一个新的 bean（会话 bean），该 bean 仅在当前 HTTP session 内有效
5. **application/global-session** （仅 Web 应用可用）： 每个 Web 应用在启动时创建一个 Bean（应用 Bean），该 bean 仅在当前应用启动时间内有效
6. **websocket** （仅 Web 应用可用）：每一次 WebSocket 会话产生一个新的 bean
#### 单例Bean的线程安全问题了解吗？
1. 单例存在线程问题，主要是因为多个线程操作同一个对象的时候是存在资源竞争的
2. 解决方法：在Bean中尽量避免定义可变的成员变量。
3. 在类中定义一个ThreadLocal成员变量，将需要的可变成员保存在ThreadLocal中
#### Bean的生命周期了解吗？
1. Bean容器找到配置文件中 Spring Bean 的定义
2. Bean 容器利用 Java Reflection API 创建一个 Bean 的实例
3. 与上面的类似，如果实现了其他 `*.Aware`接口，就调用相应的方法。NameAware传入的是Bean的名字
4. 如果有和加载这个 Bean 的 Spring 容器相关的 `BeanPostProcessor` 对象，执行`postProcessBeforeInitialization()` 方法
5. 如果 Bean 实现了`InitializingBean`接口，执行`afterPropertiesSet()`方法，如果文件中配置中的定义包含init-method属性，执行指定的方法。
6. 如果有和加载这个 Bean 的 Spring 容器相关的 `BeanPostProcessor` 对象，执行`postProcessAfterInitialization()` 方法
7. -   当要销毁 Bean 的时候，如果 Bean 实现了 `DisposableBean` 接口，执行 `destroy()` 方法。配置中定义了destory-method方法中的指定方法。
### Spring AOP
#### 对AOP了解
1. Aop:面向切面编程：能够将那些与业务无关，却为业务模块所共同调用的逻辑或责任（例如事务处理、日志管理、权限控制等）封装起来，便于减少系统的重复代码，降低模块间的耦合度，并有利于未来的可拓展性和可维护性
2. Spring AOP 就是基于动态代理的，如果要代理的对象，实现了某个接口，那么 Spring AOP 会使用 **JDK Proxy**，去创建代理对象，而对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候 Spring AOP 会使用 **Cglib** 生成一个被代理对象的子类来作为代理
3. 术语：
	1. 目标
	2. 代理
	3. 连接点
	4. 切入点
	5. 通知
	6. 切面
	7. 织入：将通知应用到目标对象，进而生成代理对象的过程动作
#### Spring Aop和AspectJ Aop的区别
1. 一个运行时增强，一个是编译时增强，一个是基于代理一个基于字节码
2. 切面多的时候时使用AspectJ

