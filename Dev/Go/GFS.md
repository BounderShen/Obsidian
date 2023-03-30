### GFS文件系统

### 简历

1. 写时复制技术
2. 放置策略
3. 存储垃圾回收
4. 新旧检测技术

#### 词汇

1. internal fragmentation
2. sequentially
3. overhead
4. persistent
5. compact
6. vanish spontaneously 
7. mutation

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

##### 当面临主机或者chunkServer出现错误时如何保证一致性

##### 操作日志

1. 只有本地和远程刷新了相应的远程记录到磁盘，才相应客户端操作

##### 主服务器

1. 主服务器通过重放操作日志来恢复其文件系统状态。为了最小化启动时间，我们必须保持日志小。每当日志增长超过一定大小时，master 就会检查其状态，以便它可以通过从本地磁盘加载最新的检查点并仅重放

2. 之后的日志记录数量有限。检查点是一种紧凑的 B-tree 形式，可以直接映射到内存中，用于命名空间查找，无需额外解析。这进一步加快了恢复速度并提高了可用性。

   因为建立检查点可能需要一段时间，所以 master 的内部状态的结构使得可以在不延迟传入突变的情况下创建新的检查点。 master 切换到一个新的日志文件，并在一个单独的线程中创建新的检查点。新检查点包括切换前的所有突变。对于拥有几百万个文件的集群，它可以在一分钟左右创建。完成后，它会在本地和远程写入磁盘。

   恢复只需要最新的完整检查点和后续日志文件。较旧的检查点和日志文件可以自由删除，但我们保留了一些以防止灾难。检查点期间的失败不会影响正确性，因为恢复代码会检测并跳过不完整的检查点。

#### 一致性模型

##### 通过GFS保证一致性

##### 对应用的影响

1. 依靠附加适应宽松一致性模型
2. 在一个典型的用途中，编写器从头到尾生成一个文件。它在写入所有数据后自动将文件重命名为永久名称，或者定期检查已成功写入多少。检查点还可能包括应用程序级校验和。读取器仅验证和处理直到最后一个检查点的文件区域，该检查点已知处于已定义状态
3. 与随机写入相比，追加对应用程序故障的效率和弹性要高得多。检查点允许写入者以增量方式重新启动并阻止读取者处理成功写入的内容

#### 系统交互

##### 租约变更顺序

1. 使用租约来维护副本之间一致的突变顺序

2. 由master选中一个副本为primary，且选择为块为所有的变更顺序，所有的变更都按此应用顺序

3. 租用机制旨在最大限度地减少 master 的管理开销。租约的初始超时为 60 秒。但是，只要块正在发生变化，主块就可以无限期地请求并通常从主块接收扩展。这些扩展请求和授权是搭载在 master 和所有 chunkservers 之间定期交换的 HeartBeat 消息上的。

   master 有时可能会在租约到期之前尝试撤销租约（例如，当 master 想要禁用正在重命名的文件上的突变时）。即使 master 失去了与 primary 的通信，它也可以在旧租约到期后安全地向另一个副本授予新租约

![Snipaste_2023-03-21_10-20-41](E:\Snipaste_2023-03-21_10-20-41.png)

1. 客户端向主服务器询问哪个块服务器持有该块的当前租约以及其他副本的位置。如果没有人有租约，则主人将租约授予它选择的副本
2. master 回复主副本的身份和另一个（次要）副本的位置。客户端缓存此数据以备将来更改。只有当 primary 时才需要再次联系 master
3. 客户端将数据推送到所有副本。客户端可以按任何顺序执行此操作。每个 chunkserver 都会将数据存储在内部 LRU 缓冲区缓存中，直到数据被使用或老化。通过将数据流与控制流解耦，我们可以通过基于网络拓扑调度昂贵的数据流来提高性能，而不管哪个 chunkserver 是主要的
4. 一旦所有副本都确认接收到数据，客户端就会向主副本发送写入请求。该请求标识了之前推送到所有副本的数据。 primary 为它收到的所有变更分配连续的序列号，可能来自多个 clients，这提供了必要的序列化。它按序列号顺序将变更应用于其自己的本地状态
5. primary 将写入请求转发给所有辅助副本。每个次要副本都按照主要副本分配的相同序列号顺序应用突变
6. secondary都回复primary表示已经完成操作
7. primary回复client。在任何副本中遇到的任何错误都会报告给客户端。如果出现错误，写入可能已在主要副本和次要副本的任意子集上成功。 （如果它在主区域失败，它就不会被分配序列号并被转发。）客户端请求被认为失败，修改后的区域处于不一致状态。我们的客户端代码通过重试失败的突变来处理此类错误。它将在步骤 (3) 到 (7) 中进行几次尝试，然后再回退到从写入开始重试

##### 写入的文件较大或者超出块边界

1. 采用多个写入操作，遵循上述流程，但是会与其他客户端的并发操作交错和覆盖，因此一个文件区域可能包含来自不同客户端的片段，使文件处于未定义的状态

#### 数据流

1. 我们将数据流与控制流分离，以有效地使用网络。当控制从客户端流向主服务器，然后流向所有辅助服务器时，数据以流水线方式沿着精心挑选的 chunkservers 链线性推送。我们的目标是充分利用每台机器的网络带宽，避免网络瓶颈和高延迟链路，并最大限度地减少推送所有数据的延迟
2. 为了避免网络瓶颈和高延迟，采用网络拓扑中没有接受到数据的最近的机器，根据IP地址计算距离
3. 通过流水线化TCP连接上的数据传输来最小化延迟，一旦 chunkserver 收到一些数据，它就会立即开始转发。流水线对我们特别有帮助，因为我们使用具有全双工链路的交换网络。立即发送数据不会降低接收速率。在没有网络拥塞的情况下，将 B 个字节传输到 R 个副本的理想耗用时间是 B/T + RL，其中 T 是网络吞吐量，L 是在两台机器之间传输字节的延迟。我们的网络链路通常为 100 Mbps (T)，而 L 远低于 1 毫秒。

#### 原子记录追加

#### 快照

1. 快照几乎瞬间复制文件或目录树，同时最大限度地减少正在进行的突变的任何中断，通常用来创建副本的副本，或者在试验更改之前检查当前的，这些更改可以在以后轻松提交和回滚
2. **`写时复制技术：延迟复制，当 master 收到一个快照请求时，它首先撤销对它要快照的文件中的块的任何未完成的租约。这确保了对这些块的任何后续写入都需要与 master 交互以找到租约持有者。这将使 master 有机会首先创建块的新副本`**
3. 在租约被撤销或到期后，主服务器将操作记录到磁盘。然后，它通过复制源文件或目录树的元数据，将此日志记录应用到其内存中状态。新创建的快照文件指向与源文件相同的区块
4. 快照之后，客户端想要写入，会向主机发送一个请求寻找当前租约持有者。***主程序注意到块C的引用计数大于1。它推迟对客户端请求的回复，而是选择新的数据块***为什么呢？继续写入会产生什么影响
5. 它要求每个拥有C的当前副本的块服务器创建一个名为C‘的新块。通过在与原始数据块相同的数据块服务器上创建新数据块，我们确保可以在本地复制数据，主机向一个副本授予对新块C‘的租约，并回复客户端，客户端可以正常写入块，而不知道它是从现有块创建的

#### 主操作

主服务器执行所有名称空间操作。此外，它还管理整个系统中的区块副本：它做出放置决策，创建新的区块，从而创建副本，并协调各种系统范围的活动，以保持完全复制区块，平衡所有区块服务器上的负载，并回收未使用的存储

##### 命名空间管理和锁

1. GFS在逻辑上将其命名空间表示为将完整路径名映射到元数据的查找表。使用前缀压缩，可以在内存中高效地表示该表。名称空间树中的每个节点(绝对文件名或绝对目录名)都有一个关联的读写锁

#### 放置策略

它通常有数百台块服务器，分布在许多机架上。这些块服务器又可以从相同或不同机架上的数百个客户端访问。不同机架上的两台机器之间的通信可能会跨越一个或多个网络交换机。此外，进出机架的带宽可能小于机架内所有机器的总和带宽。多级分布对分布数据的可伸缩性、可靠性和可用性提出了独特的挑战。

1. 块副本放置策略有两个目的：最大化数据可靠性和可用性，最大化网络带宽利用率。对于这两种情况，仅将副本分散在机器上是不够的，这只会防止磁盘或机器故障，并充分利用每台机器的网络带宽。我们还必须跨机架分布数据块副本。这可确保即使整个机架损坏或脱机(例如，由于网络交换机或电源电路等共享资源故障)，数据块的某些副本仍将存活并保持可用。这还意味着，区块的流量，尤其是读取流量，可以利用多个机架的聚合带宽。另一方面，写入流量必须流经多个机架，这是我们心甘情愿做出的权衡

##### 副本放置策略：在分布式存储系统选择合适的位置来存储数据副本，提高系统的可用性和可靠性，最大化带宽的利用率

1. 副本放置在不同的机架或数据中心：将副本存储在不同的地理位置上，可以防止单点故障和数据丢失
2. 副本放置在不同的存储介质上：将副本存储在不同类型的存储介质上，例如磁盘和固态硬盘，可以提高系统的性能和容错能力
3. 副本放置在不同的节点上：将副本存储在不同的节点上，可以防止单点故障，同时还可以提高系统的负载均衡能力
4. 副本放置在与客户端最近的节点上：将副本存储在距离客户端最近的节点上，可以减少数据传输的延迟和网络带宽的消耗，提高系统的响应速度和性能
5. 副本放置在故障概率较低的节点上：将副本存储在故障概率较低的节点上，可以降低数据丢失和系统宕机的风险，提高系统的可用性和稳定性

#### 创建、重新复制、重新平衡

1. 当主服务器创建一个chunk时，放置最初为空的副本。原因：我们希望在磁盘空间利用率低于平均水平的区块服务器上放置新的副本，随着时间的推移，这将使区块服务器上的磁盘利用率达到均衡。
2. 我们希望限制每个区块服务器上最近创建的数量，创建的成本很低，但是可靠的预测即将到来繁重的写入，因为块是在写入时创建，并且在我们的追加一次读取多次的工作负载中，它们通常在完全写入后实际上变为只读。(3)如上所述，我们希望跨机架分布数据块的副本

##### 主副本重新复制低于用户指定目标的可用副本的

1. 发生这种情况的原因有很多：区块服务器变得不可用，它报告其副本可能已损坏，它的一个磁盘因错误而被禁用，或者提高了复制目标。需要重新复制的每个块都根据几个因素确定优先级
2. 其一是距离复制目标还有多远。例如，我们对丢失两个副本的块给予比只丢失一个副本的块更高的优先级。此外，我们更喜欢首先为实时文件重新复制块，而不是属于最近删除的文件的块
3. 为了最大限度地减少故障对正在运行的应用程序的影响，我们提高了阻碍客户端进程的任何块的优先级
4. 主服务器挑选最高优先级的块，并通过指示某个块服务器直接从现有的有效副本复制块数据来“克隆”它。新副本的放置目标与创建时的目标类似：均衡磁盘空间利用率，限制任何单个区块服务器上的活动克隆操作，以及跨机架分布副本
5. 为了防止克隆流量超过客户端流量，主服务器会限制集群和每个块服务器的活动克隆操作的数量。此外，每个块服务器通过限制其对源块服务器的读取请求来限制其在每个克隆操作上花费的带宽量
6. 主服务器定期重新平衡副本：它检查当前的副本分发，并移动副本以实现更好的磁盘空间和负载平衡。同样，在此过程中，主服务器会逐渐填充新的区块服务器，而不是立即用新的区块和随之而来的繁重的写入流量来淹没它。新复制品的放置标准类似于上面讨论的标准。此外，主服务器还必须选择要删除的现有副本服务器。一般来说，它倾向于删除空闲空间低于平均水平的区块服务器上的那些服务器，以平衡磁盘空间使用

#### 垃圾收集

删除文件后，GFS不会立即回收可用物理存储。它只在文件和区块级别的常规垃圾回收期间延迟执行此操作

##### 机制

1. 当主程序删除文件时，会记录删除操作，不会立即回收资源而是将文件名命名为包含删除时间戳的隐藏文件
2. master在主程序定期扫描文件系统命名空间期间，如果任何此类隐藏文件的存在时间超过三天(间隔是可配置的)，它会将其删除
3. 在此之前，该文件仍然可以使用新的特殊名称读取，并且可以通过将其重命名为Normal来恢复删除
4. 当隐藏文件从命名空间中移除时，其内存中元数据将被擦除。这实际上切断了它与所有数据块的链接
5. 在块命名空间的类似常规扫描中，主程序识别孤立的块(即，无法从任何文件访问的块)，并擦除这些块的元数据。在与主服务器定期交换的心跳消息中，每个块服务器报告其拥有的块的子集，主服务器用不再存在于主服务器的元数据中的所有块的标识进行回复。区块服务器可以自由删除这些区块的副本

##### 谈论

1. 分布式垃圾收集要在编程语言的上下文中找到复杂的解决方案，但在我们的例子中，它非常简单。我们可以很容易地识别对块的所有引用：它们位于由主服务器独占维护的文件到块的映射中
2. 我们还可以轻松地识别所有块副本：它们是每个块服务器上指定目录下的Linux文件，主设备不知道的任何这样的复制品都是“垃圾”

##### 存储垃圾回收方法

1. 组件故障常见的大规模分布式系统中，简单可靠。块创建可能在一些块服务器上成功，但在其他块服务器上不成功，留下主服务器不知道存在的副本。副本删除消息可能会丢失，主服务器必须记住在发生故障时重新发送它们，无论是它自己的还是块服务器的
2. 其次，它将存储回收合并到主服务器的常规后台活动中，例如定期扫描命名空间和与块服务器握手。因此，它是分批完成的，成本是摊销的。此外，只有在主人相对自由的时候才会这样做。主人可以更迅速地对需要及时关注的客户请求做出响应
3. 第三，延迟回收存储提供了一张安全网，防止意外、不可逆转的删除
4. 主要的缺点是延迟有时会阻碍用户在存储紧张时微调使用情况。重复创建和删除临时文件的应用程序可能无法立即重新使用存储。如果删除的文件再次被显式删除，我们可以通过加快存储回收来解决这些问题。我们还允许用户对命名空间的不同部分应用不同的复制和回收策略。例如，用户可以指定存储某个目录树内的文件中的所有块而不进行复制，并且立即从文件系统状态中不可撤销地移除任何已删除的文件

### 陈旧副本检测

1. 如果区块服务器发生故障并在区块关闭时错过区块的突变，则区块副本可能会变得陈旧。对于每个块，主服务器维护一个块版本号，以区分最新和过时的副本

2. 每当主服务器授予块的新租约时，它都会增加块版本号，并通知最新的副本。主服务器和这些副本服务器都以其持久状态记录新版本号。这在通知任何客户端之前发生，因此在它可以开始写入区块之前发生。如果另一个副本当前不可用，则其区块版本号将不会提前。当块服务器重新启动时，主服务器将检测到该块服务器具有过时的副本，并报告其组块集及其关联的版本号。如果主服务器看到1.的版本号大于其记录中的版本号，则主服务器会认为它在授予租约时失败，因此会将较高的版本视为最新版本
3. 主服务器在其常规垃圾收集中删除过时的副本。在此之前，当它回复客户端对区块信息的请求时，它实际上会认为过时的副本根本不存在。作为另一种保护措施，当主服务器通知客户端哪个块服务器持有对块的租用时，或者当它在克隆操作中指示块服务器从另一个块服务器读取块，主服务器包括块版本号。客户端或块服务器在执行操作时验证版本号，以便始终访问最新数据

## 容错和诊断

通过内置工具进行诊断

### 高可用

通过快速恢复和复制实现高可用

#### 快速恢复

1. 主服务器和块服务器都被设计为恢复其状态并快速启动（无论如何终止）

#### 块复制

1. 用户可以为文件命名空间的不同部分指定不同的复制级别。默认是3
2. 在块服务器脱机或通过校验和验证检测损坏的副本时，主克隆根据需要复制现有副本以保持每个块的完全复制(请参见第5.2节)。虽然复制为我们提供了很好的服务，但我们正在探索其他形式的跨服务器冗余，如奇偶校验或擦除码，以满足我们日益增长的只读存储需求。我们预计，在我们非常松散耦合的系统中实施这些更复杂的冗余方案是具有挑战性的，但却是可管理的，因为我们的流量主要由追加和读取而不是小的随机写入主导

#### 数据完整性

##### 问题

1. 如何通过检验码知道哪一个

1. 对于坏掉的64kb块，每个拥有对应的32位。和元数据一样，校验应该保存在内存中，并通过日志记录一起持久地存储
2. 对于读取，chunkserver在将任何数据返回给请求者(无论是客户端还是另一个chunkserver)之前，都会验证与读取范围重叠的数据块的校验和
3. 块服务器将不会传播损坏到其他机器。如果块与记录的校验和不匹配，`chunkserver`将错误返回给请求者，并将不匹配报告给主服务器。作为响应，请求者将从其他副本中读取数据，而主服务器将从另一个副本中克隆数据块。在一个有效的新副本到位之后，主服务器指示报告不匹配的`chunkserver`删除它的副本
4. 校验和对读取性能的影响很小，原因有几个。由于我们的大多数读取至少跨越几个块，所以我们只需要读取和校验相对少量的额外数据进行验证。通过尝试在校验和块边界对齐读取，GFS客户端代码进一步减少了这种开销。此外，在chunkserver上的校验和查找和比较是在没有任何I/O的情况下完成的，并且校验和计算通常可以与I/O重叠
5. 校验和计算针对追加到块末尾的写操作进行了大量优化(与覆盖现有数据的写操作相反)，因为它们在我们的工作负载中占主导地位。我们只是增量地更新最后一个部分校验和块的校验和，并为任何由追加填充的全新校验和块计算新的校验和。即使最后一个部分校验和块已经损坏，而我们现在未能检测到它，新的校验和值将与存储的数据不匹配，并且在下一次读取块时将像往常一样检测到损坏
6. <u>相反，如果写操作覆盖了块的现有范围，则必须读取并验证被覆盖范围的第一个和最后一个块，然后执行写操作</u>
7. 最后计算并记录新的校验和。如果在部分覆盖第一个和最后一个块之前不验证它们，新的校验和可能会隐藏未覆盖区域中存在的损坏。在空闲期间，chunkserver可以扫描和验证非活动块的内容。这允许我们检测很少读取的数据块中的损坏。一旦检测到损坏，主服务器可以创建一个新的未损坏的副本并删除损坏的副本。这可以防止一个不活跃但已损坏的块副本欺骗主服务器，使其认为它有足够多的块的有效副本

#### 诊断工具

GFS服务器生成诊断日志，记录许多重要事件(例如chunkserver的上升和下降)以及所有RPC请求和响应。这些诊断日志可以自由删除，不会影响系统的正确性。然而，我们尽量在空间允许的范围内保留这些日志

RPC日志包括在线路上发送的确切请求和响应，除了正在读写的文件数据。通过匹配请求与应答并整理不同机器上的RPC记录，我们可以重建整个交互历史以诊断问题。日志还可以作为负载测试和性能分析的跟踪

日志记录对性能的影响很小(其好处远远超过了它)，因为这些日志是按顺序和异步写入的。最近的事件也被保存在内存中，并可用于持续的在线监控

## 测量

### 微型基准

#### 




