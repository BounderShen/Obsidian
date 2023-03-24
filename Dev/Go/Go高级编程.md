### 面向并发内存模型

#### Goroutine和系统线程

1. 每个系统级线程都会有一个固定大小的栈（一般默认可能是2MB），这个栈主要用来保存函数递归调用时参数和局部变量。造成的问题是对于需要很小的栈空间的线程来说是一个巨大的浪费，二是对于少数需要巨大栈空间的线程来说会面临着溢出的风险
2. 一个Goroutine会以一个很小的栈启动（可能是2KB或4KB），当遇到深度递归导致当前栈空间不足时，Goroutine会根据需要动态地伸缩栈的大小（主流实现中栈的最大值可达到1GB）

##### 基于sync实现单例模式

```go
var (
    instance *singleton
    once     sync.Once
)
func Instance() *singleton {
    //保证函数只执行一次
    once.Do(func() {
        instance = &singleton{}
    })
    return instance
}
```

#### 顺序一致性内存

1. 在Go语言中，同一个Goroutine线程内部，顺序一致性内存模型是得到保证的。但是不同的Goroutine之间，并不满足顺序一致性内存模型，需要通过明确定义的同步事件来作为同步的参考

#### 初始化顺序

1. 包中包，先导入里面的包，对常量->全局变量进行初始化->初始化函数，

#### Go协程的创建

1. 会在函数返回前创建Go协程

#### 基于通道通信

1. **无缓存的Channel上的发送操作总在对应的接收操作完成前发生**

### 常见的并发模式

#### 并发版本的HelloWorld

```go
func main() {
    var wg sync.WaitGroup
    // 开N个后台打印线程
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func() {
            fmt.Println("你好, 世界")
            wg.Done()
        }()
    }
    // 等待N个后台线程完成
    wg.Wait()
}
```

#### 生产者和消费者模型

```go
func Producer(factor int, out chan<- int) {
    for i := 0; ; i++ {
        out <- i*factor
    }
}
// 消费者
func Consumer(in <-chan int) {
    for v := range in {
        fmt.Println(v)
    }
}
func main() {
    ch := make(chan int, 64) // 成果队列
    go Producer(3, ch) // 生成 3 的倍数的序列
    go Producer(5, ch) // 生成 5 的倍数的序列
    go Consumer(ch)    // 消费 生成的队列
    // Ctrl+C 退出
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    fmt.Printf("quit (%v)\n", <-sig)
}
```

#### 发布订阅模型

1. 发布者的基本信息
2. 拥有添加/删除订阅者，创建发布者，发布功能
3. 修改采用了加互斥锁

```go
// Package pubsub implements a simple multi-topic pub-sub library.
package pubsub
import (
    "sync"
    "time"
)
type (
    subscriber chan interface{}         // 订阅者为一个管道
    topicFunc  func(v interface{}) bool // 主题为一个过滤器
)
// 发布者对象
type Publisher struct {
    m           sync.RWMutex             // 读写锁
    buffer      int                      // 订阅队列的缓存大小
    timeout     time.Duration            // 发布超时时间
    subscribers map[subscriber]topicFunc // 订阅者信息
}
// 构建一个发布者对象, 可以设置发布超时时间和缓存队列的长度
func NewPublisher(publishTimeout time.Duration, buffer int) *Publisher {
    return &Publisher{
        buffer:      buffer,
        timeout:     publishTimeout,
        subscribers: make(map[subscriber]topicFunc),
    }
}
// 添加一个新的订阅者，订阅全部主题
func (p *Publisher) Subscribe() chan interface{} {
    return p.SubscribeTopic(nil)
}
// 添加一个新的订阅者，订阅过滤器筛选后的主题
func (p *Publisher) SubscribeTopic(topic topicFunc) chan interface{} {
    ch := make(chan interface{}, p.buffer)
    p.m.Lock()
    p.subscribers[ch] = topic
    p.m.Unlock()
    return ch
}
// 退出订阅
func (p *Publisher) Evict(sub chan interface{}) {
    p.m.Lock()
    defer p.m.Unlock()
    delete(p.subscribers, sub)
    close(sub)
}
// 发布一个主题
func (p *Publisher) Publish(v interface{}) {
    p.m.RLock()
    defer p.m.RUnlock()
    var wg sync.WaitGroup
    for sub, topic := range p.subscribers {
        wg.Add(1)
        go p.sendTopic(sub, topic, v, &wg)
    }
    wg.Wait()
}
// 关闭发布者对象，同时关闭所有的订阅者管道。
func (p *Publisher) Close() {
    p.m.Lock()
    defer p.m.Unlock()
    for sub := range p.subscribers {
        delete(p.subscribers, sub)
        close(sub)
    }
}
// 发送主题，可以容忍一定的超时
func (p *Publisher) sendTopic(
    sub subscriber, topic topicFunc, v interface{}, wg *sync.WaitGroup,
) {
    defer wg.Done()
    if topic != nil && !topic(v) {
        return
    }
    select {
    case sub <- v:
    case <-time.After(p.timeout):
    }
}
```

##### 调用

```go
import "path/to/pubsub"
func main() {
    p := pubsub.NewPublisher(100*time.Millisecond, 10)
    defer p.Close()
    all := p.Subscribe()
    golang := p.SubscribeTopic(func(v interface{}) bool {
        if s, ok := v.(string); ok {
            return strings.Contains(s, "golang")
        }
        return false
    })
    p.Publish("hello,  world!")
    p.Publish("hello, golang!")
    go func() {
        for  msg := range all {
            fmt.Println("all:", msg)
        }
    } ()
    go func() {
        for  msg := range golang {
            fmt.Println("golang:", msg)
        }
    } ()
    // 运行一定时间后退出
    time.Sleep(3 * time.Second)
}
```

#### 控制并发数

```go
import (
    "golang.org/x/tools/godoc/vfs"
    "golang.org/x/tools/godoc/vfs/gatefs"
)
func main() {
    fs := gatefs.New(vfs.OS("/path"), make(chan bool, 8))
    // ...
}
```

