### GFS文件系统

#### 词汇

1. internal fragmentation
2. sequentially
3. overhead
4. persistent

#### 问题

##### 文件通过附加新数据而不是覆盖现有数据来改变

##### 快照以低成本创建文件或目录树的副本

##### 架构

1. A G F S c l u s t e r c o n s i s t s o f a s i n g l e master and multiple
   chunkservers and is accessed by multiple clients,

##### 独一无二的标识
each chunk identified by an immutable and globally unique 64 bit chunk
handle assigned by the master at the time of chunk creation

##### 客户端缓存

客户端和 chunkserver 都不缓存文件数据。客户端缓存几乎没有什么好处，因为大多数应用程序流式传输大量文件或工作集太大而无法缓存。没有它们可以通过消除缓存一致性问题来简化客户端和整个系统。（然而，客户端会缓存元数据。）Chunkservers 不需要缓存文件数据，因为块存储为本地文件，因此 Linux 的缓冲区缓存已经将经常访问的数据保存在内存中。

##### 架构原理

1. 客户端向master获取到对应文件的位置和处理客户端根据这些信息，向chunk服务器进行读写，

##### 请求过载

1. 存储此可执行文件的少数 `chunkservers` 因数百个同时请求而超载。我们通过以更高的复制因子存储此类可执行文件并使批处理队列系统错开应用程序启动时间来解决此问题。一个潜在的长期解决方案是允许客户端在这种情况下从其他客户端读取数据。

##### what is the version number

the version number is purpose make master can find which server has the newest chunk

avoiding to build two primary for chunk,

##### split brain 

1. until lease least 
2. start to build a primary

##### 两阶段提交

1. primary 向 secongdary提问你可以做这个，
2. second同意后可以去做