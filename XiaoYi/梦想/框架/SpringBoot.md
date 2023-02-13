## Java Basics
### Spring Boot -continued
#### WebSocket and STOMP
1. webSocket是一种低级通信协议，定义字节如何为包含信息的帧（二进制或者文本信息）.
2. STOMP是一个简单的基于文本的消息协议
3. 代理程序不用关心协议的问题，接收方会将协议自动转换为发送方的协议
#### WebSocket 例子
~~~
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
	
}
~~~
1. 创建一个WebSocket配置类
2. 第一个方法：创建一个消息代理端点，不支持websocket就用JS
3. 第二个方法：创建路由转向指定的断点，以及指定前缀是xxx就转到控制类进行执行 
### 包装应用
1. Jar
2. War
##### 包装例子
1. clean
2. package
##### 运行方法
1. 找到target下的jar即可运行
2. 切换到指定目录下，使用Java -jar target/xx进行运行
##### 使用参数运行
1. 后面添加--server.port=8080
2. --trace 跟踪
### 网页服务和API
#### 网页服务

##### 什么是网页服务
1. 在两个完全不同的系统中分享数据
##### 网页通信
1. 使用JSON或者XML语言进行通信
#### 网页服务的优势
##### 优势
1. 重用
#### 网页服务和API和微服务
##### API
1. 轻量级
2. 需要解压缩数据
3. 设备限制带宽
4. 所有网页服务都是API，但不是所有的API都是
##### 微服务
1. 类似API
2. 独立组件


