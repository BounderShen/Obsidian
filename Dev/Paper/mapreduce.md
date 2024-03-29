#### 摘要
MapReduce是一种编程模型和相关实现，用于处理和生成大数据集。用户指定一个map函数来处理键/值对以生成一组中间键/值对，以及一个reduce函数来合并与同一中间键关联的所有中间值。许多真实世界的任务都可以在这个模型中表达，如论文所示。使用这种功能风格编写的程序会自动并行化，并在大量普通计算机群集上执行。运行时系统负责分区输入数据、调度程序跨一组机器执行、处理机器故障和管理所需的机器间通信等细节。这使得没有任何并行和分布式系统经验的程序员可以轻松利用大型分布式系统的资源。
我们MapReduce实现运行在大规模普通计算机群集上，并具有高可扩展性：典型的MapReduce计算可以在数千台计算机上处理数TB级别的数据。程序员发现该系统易于使用：已经实施了数百个MapReduce程序，并且每天有超过1000个MapReduce作业在Google集群上执行。
#### 1.介绍
在过去的五年中，谷歌的作者和许多其他人实现了数百个特殊用途计算，处理大量原始数据（如爬取文档、Web请求日志等），以计算各种派生数据，例如倒排索引、Web文档图形结构的各种表示形式、每个主机爬取页面数量的摘要、给定日期内最常见查询集合等。大多数这样的计算在概念上都很简单。然而，输入数据通常很大，并且必须将计算分布在数百或数千台机器上才能在合理时间内完成。如何并行化计算、分发数据和处理故障问题共同使得原本简单的计算变得复杂起来。

作为对这种复杂性的反应，我们设计了一个新抽象层次结构，允许我们表达我们试图执行但隐藏了并行化、容错性、数据分发和负载平衡混乱细节中所涉及到的简单运算库。我们抽象层次受Lisp和许多其他函数语言中存在map和reduce基元启示而来。我们意识到，我们大部分运算都涉及将map操作应用于输入中每个逻辑“记录”，以便计算一组中间键/值对；然后将reduce操作应用于所有共享相同键的值，以便适当地组合派生数据。我们使用具有用户指定map和reduce操作的函数模型，可以轻松并行化大型计算，并将重新执行用作容错的主要机制。

这项工作的主要贡献是一个简单而强大的接口，使得大规模计算的自动并行化和分布成为可能，并结合了这个接口的实现，在普通PC集群上获得高性能。
第2节描述了基本编程模型并给出了几个示例。第3节描述了MapReduce接口在我们基于集群的计算环境中量身定制的实现。第4节描述了我们发现有用的编程模型几个细化方面。第5节对我们实现各种任务时进行性能测量。第6节探讨Google内部使用MapReduce以及将其作为重写生产索引系统基础时所遇到经验。第7节讨论相关和未来工作。

#### 2.编程模型
计算过程接受一组输入键/值对，并生成一组输出键/值对。MapReduce库的用户通过两个函数来表达计算：Map和Reduce。
由用户编写的Map函数接受一个输入对并产生一组中间键/值对。MapReduce库将所有与相同中间键I相关联的中间值分组在一起，并将它们传递给Reduce函数。
也由用户编写的Reduce函数接受一个中间键I和该键的一组值。它合并这些值以形成可能更小的值集合。通常每次调用Reduce只会产生零个或一个输出值。通过迭代器向用户提供了中间结果，从而可以处理无法放入内存的大型数列数据。
##### 2.1例子
考虑在大量文档中计算每个单词出现次数的问题。用户将编写类似以下伪代码的代码：
map(String key, String value):
// key: document name
// value: document contents for each word w in value:
EmitIntermediate(w, "1");
reduce(String key, Iterator values):
// key: a word
// values: a list of counts int result = 0;
for each v in values: result += ParseInt(v);
Emit(AsString(result));
map”函数会发出每个单词及其出现次数的计数（在这个简单的例子中只有“1”）。 “reduce”函数将特定单词发出的所有计数相加。
此外，用户编写代码填充一个MapReduce规范对象，其中包含输入和输出文件的名称以及可选调整参数。然后，用户调用MapReduce函数，并传递给它该规范对象。用户的代码与MapReduce库（用C++实现）链接在一起。附录A包含了此示例的完整程序文本。
##### 2.2类型
尽管之前的伪代码是以字符串输入和输出为基础编写的，但用户提供的映射和归约函数在概念上具有相关类型：
map         (k1,v1)        → list(k2,v2)
reduce    (k2,list(v2)) → list(v2)
输入键和值来自不同的域，而输出键和值则来自另一个域。此外，中间键和值与输出键和值来自相同的域。
我们的C++实现将字符串传递给用户定义函数，并由用户代码在字符串和适当类型之间进行转换。
##### 更多的例子
以下是一些简单的有趣程序示例，可以轻松地表示为MapReduce计算。

分布式Grep：map函数如果匹配了提供的模式，则发出一行。reduce函数是一个恒等函数，只将提供的中间数据复制到输出。

URL访问频率计数：map函数处理网页请求日志并输出hURL, 1i。reduce函数将相同URL的所有值相加，并发出hURL, 总数i对。

反向Web链接图：map函数针对在名为source的页面中找到目标URL的每个链接输出htarget, sourcei对。reduce函数连接与给定目标URL相关联的所有源URL列表，并发出该对:htarget, list(source)i

每个主机术语向量：术语向量总结了文档或一组文档中最重要单词作为hword，frequencyi对列表。 map 函数针对每个输入文档（其中主机名从文档 URL 中提取）发出 hhostname、term vector 对。 reduce 函数传递给定主机的所有按文件分割后各自生成 term vectors 。它们将这些项合并起来，丢弃不常见项，然后发出最终 hhostname、term vector 对。
倒排索引：映射函数解析每个文档，并发出一系列的单词、文档ID对。规约函数接受给定单词的所有对，排序相应的文档ID并发出一个单词、列表（文档ID）对。所有输出对的集合形成了一个简单的倒排索引。很容易扩展这个计算来跟踪单词位置。

分布式排序：映射函数从每条记录中提取键，并发出一个键、记录对。规约函数不改变所有配对关系。此计算依赖于第4.1节描述的分区设施和第4.2节描述的排序属性。

![](E:\IT\图片\Snipaste_2023-03-26_23-15-01.png)

#### 3.实现
MapReduce接口有许多不同的实现方式，正确的选择取决于环境。例如，一个实现可能适用于小型共享内存机器，另一个则适用于大型NUMA多处理器系统，还有一种则适用于更大规模的网络机群。

本节描述了针对Google广泛使用的计算环境而设计的一种实现：由交换式以太网连接在一起的廉价PC集群[4]。在我们这个环境中：
(1) 机器通常是运行Linux操作系统、配备2-4GB内存、采用双处理器x86架构。
(2) 使用普通网络硬件——通常是每台机器100兆比特/秒或1千兆比特/秒，但总体二分带宽要低得多。
(3) 集群由数百或数千台机器组成，因此机器故障很常见。
(4) 存储由直接连接到各个单独机器上的廉价IDE硬盘提供。我们自主开发了一个分布式文件系统[8]来管理这些硬盘上存储的数据。该文件系统使用复制技术，在不可靠硬件之上提供可用性和可靠性保证。
(5) 用户将作业提交给调度系统。每个作业包含一组任务，并由调度程序映射到集群中的一组可用机器。
##### 3.1执行概述
Map调用通过自动将输入数据分成一组M个拆分来在多台机器上进行分布式处理。不同的机器可以并行处理输入拆分。Reduce调用通过使用一个划分函数（例如，hash(key) mod R）将中间键空间划分为R个部分来进行分布式处理。用户指定了划分数（R）和划分函数。
图1显示了我们实现中MapReduce操作的整体流程。当用户程序调用MapReduce函数时，会发生以下操作序列（图1中编号标签对应于下面列表中的数字）：

1. 用户程序中的MapReduce库首先将输入文件拆成通常每个片段16兆字节到64兆字节大小的M份（可由用户通过可选参数控制）。然后，在一组计算机集群上启动许多程序副本。
2. 程序副本之一是特殊的——主节点。其余都是工作节点，由主节点指派任务给它们。需要指派M个map任务和R个reduce任务。主节点选择空闲工作节点，并为每个工作节点指派一个map或reduce任务。
3. 被指派执行map任务的工作节点读取相应输入拆件内容，并从其中解析出键/值对，并将每对传递给用户定义的Map函数进行处理生成中间键/值对并缓存在内存中。
4. 定期地，缓冲区内部产生的键/值对被写入本地磁盘，并通过划分函数将其划分为R个区域。这些缓冲区内部产生的键/值对在本地磁盘上的位置会传回给主节点，由主节点负责将这些位置转发给reduce工作节点。
5. 5. 当一个reduce工作进程被主节点通知这些位置时，它使用远程过程调用从映射工作进程的本地磁盘读取缓冲数据。当一个reduce工作进程读取了所有中间数据后，它按中间键对其进行排序，以便将相同键的所有出现分组在一起。排序是必要的，因为通常许多不同的键映射到同一个reduce任务。如果中间数据量太大无法放入内存，则使用外部排序。
6. reduce工作进程遍历已排序的中间数据，并针对每个唯一的中间键遇到时，将该键和相应集合的中间值传递给用户定义Reduce函数。 Reduce函数输出附加到此减少分区的最终输出文件上。
7. 当所有map任务和reduce任务都完成后，主节点会唤醒用户程序。此时，在用户程序中MapReduce调用返回到用户代码。

成功完成后，MapReduce执行结果可在R输出文件（每个减少任务一个文件，并由用户指定文件名） 中获得。通常情况下，用户不需要将这些R输出文件合并成一个文件 - 他们经常将这些文件作为输入传递给另一个MapReduce调用或从能够处理分成多个文件 的其他分布式应用程序使用它们 。
##### 3.2主数据结
主节点维护了多个数据结构。对于每个映射任务和归约任务，它存储了状态（空闲、进行中或已完成）以及工作机器的身份（对于非空闲任务）。
主节点是中间人，通过它，从映射任务到归约任务传播中间文件区域的位置。因此，对于每个已完成的映射任务，主节点存储了映射任务生成的R个中间文件区域的位置和大小。随着映射任务的完成，位置和大小信息的更新被接收。信息被逐步推送到具有正在进行的归约任务的工作机器。
##### 3.3容错
由于MapReduce库旨在使用数百或数千台机器处理大量数据，因此该库必须能够优雅地容忍机器故障。

***工作机器故障***
主节点定期向每个工作机器发送ping请求。如果在一定时间内没有收到来自工作机器的响应，则主节点将该工作机器标记为故障。由该工作机器完成的任何映射任务都将被重置回其初始空闲状态，因此可以在其他工作机器上进行调度。同样，正在失败的工作机器上进行的任何映射任务或归约任务也将被重置为空闲状态，并可以重新进行调度。

由于已完成的映射任务的输出存储在失败机器的本地磁盘上，因此无法访问，因此在故障发生时需要重新执行已完成的映射任务。而已完成的归约任务不需要重新执行，因为其输出存储在全局文件系统中。
当映射任务首先由工作机器A执行，然后由工作机器B执行（因为A失败），所有执行归约任务的工作机器都会收到重新执行的通知。任何尚未从工作机器A读取数据的归约任务将从工作机器B读取数据。

MapReduce对大规模工作机器故障具有弹性。例如，在一次MapReduce操作期间，正在运行的集群上进行网络维护，导致每次80台机器变得无法访问，持续数分钟。MapReduce主节点简单地重新执行不可达到的工作机器所完成的工作，并继续向前推进，最终完成了MapReduce操作。
***主故障***
很容易让主节点定期写入上述主数据结构的检查点。如果主节点任务死亡，则可以从最后一个检查点状态开始启动新副本。但是，考虑到只有一个主节点，其故障不太可能发生；因此，我们当前的实现在主节点故障时会中止MapReduce计算。客户端可以检查此条件，并在需要时重试MapReduce操作。
***出现故障时的语义***
当用户提供的映射和归约运算符是其输入值的确定性函数时，我们的分布式实现会产生与整个程序的非故障顺序执行所产生的输出相同的输出。

我们依赖于映射和归约任务输出的原子提交来实现这一属性。每个正在进行的任务将其输出写入私有临时文件。一个归约任务产生一个这样的文件，而一个映射任务产生R个这样的文件（每个归约任务一个）。当映射任务完成时，工作机器会向主节点发送消息，并在消息中包含R个临时文件的名称。如果主节点收到一个已经完成的映射任务的完成消息，则会忽略该消息。否则，它会将R个文件的名称记录在主数据结构中。当归约任务完成时，归约工作机器会原子地将其临时输出文件重命名为最终输出文件。如果同一个归约任务在多台机器上执行，则将为同一个最终输出文件执行多个重命名调用。我们依赖于底层文件系统提供的原子重命名操作来保证最终文件系统状态仅包含一次执行归约任务所产生的数据。

当一个reduce任务完成时，reduce工作节点以原子方式将其临时输出文件重命名为最终输出文件。如果同一个reduce任务在多台机器上执行，将会为同一个最终输出文件执行多个重命名操作。我们依赖底层文件系统提供的原子重命名操作来保证最终文件系统状态仅包含由一个reduce任务执行产生的数据。

我们的大部分map和reduce操作符都是确定性的，当这种情况下我们的语义等价于顺序执行时，这使得程序员可以很容易地推断出它们的程序行为。当map和/或reduce操作符是非确定性的时，我们提供更弱但仍合理的语义。在存在非确定性操作符的情况下，特定reduce任务R1的输出等价于非确定性程序顺序执行产生的R1输出。然而，不同的reduce任务R2的输出可能对应于非确定性程序的另一个顺序执行产生的R2输出。
考虑map任务M和reduce任务R1和R2。让e(Ri)表示提交的Ri执行（恰好有一个这样的执行）。较弱的语义是由于e(R1)可能读取由M的一个执行产生的输出，而e(R2)可能读取由M的另一个执行产生的输出。
##### 3.4本地性
在我们的计算环境中，网络带宽是相对稀缺的资源。我们通过利用输入数据（由GFS [8]管理）存储在集群中的机器的本地磁盘上这一事实来节省网络带宽。GFS将每个文件分成64 MB块，并在不同的机器上存储每个块的多个副本（通常是3个副本）。MapReduce主节点考虑输入文件的位置信息，并尝试在包含相应输入数据副本的机器上调度map任务。如果无法实现，它将尝试在距离该任务输入数据副本附近的机器上调度map任务（例如，在与包含数据的机器相同的网络交换机上的工作机器上）。在集群中的大型MapReduce操作中运行，大部分输入数据都是本地读取的，不消耗网络带宽。
##### 3.5任务粒度
我们将map阶段分为M个部分，将reduce阶段分为R个部分，如上所述。理想情况下，M和R应该远大于工作机器的数量。每个工作机器执行多个不同的任务可以改善动态负载平衡，并且在一个工作机器失败时加速恢复：它已经完成的许多map任务可以分布在所有其他工作机器上。
在我们的实现中，M和R的大小有实际限制，因为主节点必须做出O(M+R)的调度决策，并像上面描述的那样在内存中保存O(M*R)的状态。（内存使用的常数因子很小：状态中的O(M*R)部分大约是每个map任务/ reduce任务对应的一字节数据。）

此外，R通常受到用户的限制，因为每个reduce任务的输出最终都会在单独的输出文件中。在实践中，我们倾向于选择M，使得每个单独的任务大约为16 MB到64 MB的输入数据（以便上述本地性优化最为有效），并使R成为我们预计使用的工作机器数量的小倍数。我们通常使用M = 200,000和R = 5,000，在2,000个工作机器上执行MapReduce计算。
##### 3.6备份任务
MapReduce操作总时间增长的一个常见原因是“慢任务”：一台机器在计算的最后几个map或reduce任务中完成一个任务需要异常长的时间。慢任务可能出现各种各样的原因。例如，一台具有坏磁盘的机器可能会经常出现可以纠正的错误，从而将其读取性能从30 MB/s降至1 MB/s。集群调度系统可能已经在该机器上安排了其他任务，由于CPU、内存、本地磁盘或网络带宽的竞争，导致MapReduce代码执行更慢。我们最近遇到的一个问题是机器初始化代码中的一个错误，导致处理器缓存被禁用：受影响的机器上的计算速度降低了一百倍以上。
我们有一个通用机制来缓解慢任务的问题。当MapReduce操作接近完成时，主节点将剩余的正在进行的任务调度为备份执行。只要主执行或备份执行完成，任务就被标记为已完成。我们已经调整了此机制，使其通常将操作使用的计算资源增加不超过几个百分点。
我们发现，这显著减少了完成大型MapReduce操作所需的时间。例如，第5.3节中描述的排序程序，如果禁用备份任务机制，则完成需要增加44%的时间。
#### 4.改进
尽管简单地编写Map和Reduce函数提供的基本功能对于大多数需要已经足够，但我们发现一些扩展是有用的。本节将介绍这些扩展。
###### 4.1分区函数
MapReduce的用户指定他们所需的reduce任务/输出文件数量(R)。使用中间键的分区函数将数据分区到这些任务中。提供了一个默认的分区函数，它使用哈希函数（例如，“hash(key) mod R”）。这往往会产生相当平衡的分区。但在某些情况下，按照键的其他函数分区数据是有用的。例如，有时输出键是URL，我们希望同一主机的所有条目都出现在同一个输出文件中。为支持这类情况，MapReduce库的用户可以提供一个特殊的分区函数。例如，使用“hash(Hostname(urlkey)) mod R”作为分区函数会导致来自同一主机的所有URL出现在同一个输出文件中。
##### 4.2订购保证
我们保证在给定的分区内，中间键/值对按键的递增顺序处理。这个排序保证使得生成每个分区的排序输出文件变得容易，当输出文件格式需要支持通过键进行高效随机访问查找时，或者输出的用户发现数据排序很方便时，这非常有用。
##### 4.3组合函数
在某些情况下，每个map任务生成的中间键存在显著的重复，并且用户指定的Reduce函数是可交换和可结合的。第2.1节中的单词计数示例就是一个很好的例子。由于单词频率往往遵循Zipf分布，每个map任务将生成数百或数千个形如<the，1>的记录。所有这些计数都将通过网络发送到一个单独的reduce任务，然后由Reduce函数相加以产生一个数字。我们允许用户指定一个可选的Combiner函数，在将数据发送到网络之前对其进行部分合并。
Combiner函数在执行map任务的每台机器上执行。通常使用相同的代码来实现组合器和reduce函数。Reduce函数和组合器函数之间唯一的区别在于MapReduce库如何处理函数的输出。Reduce函数的输出写入最终的输出文件中。组合器函数的输出写入一个中间文件，该文件将被发送到reduce任务。
部分合并显着加速了某些类别的MapReduce操作。附录A包含了一个使用组合器的示例。
##### 4.4输入输出类型
MapReduce库提供了对几种不同格式的输入数据的支持。例如，“text”模式输入将每行视为键/值对：键是文件中的偏移量，值是行的内容。另一种常见的支持的格式存储按键排序的键/值对序列。每种输入类型的实现知道如何将自己分成有意义的范围以作为单独的map任务进行处理（例如，文本模式的范围分割确保仅在行边界处发生范围分割）。用户可以通过提供简单读取器接口的实现来为新的输入类型添加支持，尽管大多数用户只使用少量预定义的输入类型之一。
一个读取器不一定需要提供从文件中读取的数据。例如，容易定义一个读取器，从数据库中读取记录，或者从映射在内存中的数据结构中读取记录。
类似地，我们支持一组输出类型来以不同的格式生成数据，用户代码很容易为新的输出类型添加支持。
##### 4.5副作用
在某些情况下，MapReduce的用户发现从他们的map和/或reduce运算符产生辅助文件作为附加输出非常方便。我们依赖应用程序编写者使这样的副作用具有原子性和幂等性。通常，应用程序会写入一个临时文件，并在完全生成后将此文件进行原子重命名。
我们不提供对由单个任务产生的多个输出文件的原子两阶段提交的支持。因此，具有跨文件一致性要求的多个输出文件的任务应该是确定性的。在实践中，这个限制从未成为问题。
##### 4.6跳过不良记录
有时用户代码中存在错误，导致Map或Reduce函数在某些记录上确定性地崩溃。这样的错误会阻止MapReduce操作完成。通常的做法是修复错误，但有时这是不可行的；也许错误在一个没有源代码的第三方库中。此外，有时忽略一些记录是可以接受的，例如对大数据集进行统计分析时。我们提供了一种可选的执行模式，其中MapReduce库检测哪些记录会导致确定性崩溃，并跳过这些记录以推进进程。
每个工作进程都安装了一个信号处理程序，用于捕获分段违规和总线错误。在调用用户Map或Reduce操作之前，MapReduce库将参数的序列号存储在全局变量中。如果用户代码生成信号，信号处理程序将发送一个“最后的呼吸”UDP数据包，其中包含序列号，发送至MapReduce主节点。当主节点在特定记录上看到超过一个失败时，它表示在发出相应的Map或Reduce任务的下一次重新执行时应跳过该记录。
##### 4.7本地执行
在Map或Reduce函数中调试问题可能会很棘手，因为实际的计算发生在一个分布式系统中，通常在数千台机器上进行，由主节点动态地进行工作分配决策。为了帮助促进调试、性能分析和小规模测试，我们开发了一个MapReduce库的替代实现，它在本地机器上顺序执行MapReduce操作的所有工作。为用户提供了控件，以便计算可以限制在特定的map任务上。用户使用特殊标志调用他们的程序，然后可以轻松地使用任何他们发现有用的调试或测试工具（例如gdb）。
##### 4.8状态信息
主节点运行内部HTTP服务器，并导出一组人类可读的状态页面。状态页面显示计算的进度，例如已完成多少任务，正在进行多少任务，输入字节数，中间数据字节数，输出字节数，处理速率等。页面还包含每个任务生成的标准错误和标准输出文件的链接。用户可以使用这些数据来预测计算需要多长时间，以及是否应该向计算添加更多资源。这些页面还可以用于确定计算是否比预期慢得多。
此外，顶层状态页面显示了哪些工作进程失败了，以及它们在失败时正在处理哪些map和reduce任务。在尝试诊断用户代码中的错误时，这些信息非常有用。
##### 4.9计数器
MapReduce库提供了一个计数器功能，用于计算各种事件的发生次数。例如，用户代码可能想要计算处理的单词总数或索引的德语文档数量等。
要使用此功能，用户代码创建一个命名计数器对象，然后在Map和/或Reduce函数中适当地增加计数器。例如：
Counter* uppercase;
uppercase = GetCounter("uppercase");
map(String name, String contents):
for each word w in contents:
if (IsCapitalized(w)):
uppercase->Increment();
EmitIntermediate(w, "1");
单个工作机器的计数器值定期传播到主节点（附带在ping响应中）。主节点汇总成功的map和reduce任务的计数器值，并在MapReduce操作完成时将它们返回给用户代码。当前计数器值也显示在主节点状态页面上，以便人类可以观察实时计算的进度。在聚合计数器值时，主节点消除了执行相同map或reduce任务的重复执行的影响，以避免重复计数。（重复执行可能来自于我们使用的备份任务以及由于故障而重新执行任务。）
MapReduce库自动维护一些计数器值，例如处理的输入键/值对的数量和生成的输出键/值对的数量。
用户发现计数器功能对于检查MapReduce操作的行为非常有用。例如，在某些MapReduce操作中，用户代码可能想要确保生成的输出对数恰好等于处理的输入对数，或者处理的德语文档比例在总处理的文档数量的可接受比例范围内。





