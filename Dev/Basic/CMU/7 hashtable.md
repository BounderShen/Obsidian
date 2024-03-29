#### 前言
###### 数据结构
1. 内部元数据
2. 核心数据存储
3. 临时数据结构
4. 表索引
##### 设计决策
1. 如何在内存/页面中布局数据结构，哪些消息执支持高效地访问
2. 多个线程在同一时间访问数据结构没有出现问题
##### 静态哈希表
1. 从逻辑上删除一个key，线程回去找会不存在，但是物理上还是存在的
2. 关注的是数据结构的物理完整性，而不是逻辑上的
3. 实际上哈希中存储键是存储一个指针指向键的值
4. 哈希表，要在内存量和存储空间取得平衡
##### 哈希函数测试
1. 在32、64、128出现尖端，因为正好填满cache line（CPU和主存之间数据传输最小单位），数据对齐，数据吞吐量刚好最佳，一次处理拿到想要的数据
2. S3、EBS buket加密性数据库
#### 哈希函数
1. Facebook XXHash：不论键值是多少，吞吐量都是巨大的
2. 并没有使用哈希加密函数，因为想要速度更快且低冲突
3. MD5加密算法，可以通过彩虹表破解且速度慢
#### 静态哈希方案
1. 分配的时候就知道存储的数量
2. 容量满了，需要扩容，本质上需要扩容到原来的两倍；需要将第一个表中的元素复制到第二个上，实际上需要重新哈希并存储，代价过高
##### 线性探测哈希
***问题***
1. 找不到会空槽发生什么
1. 解决哈希冲突方法：如果说发生哈希冲突，顺着这个槽往下找到空槽并存储，直到末尾还是还没有就重头开始找到为止
2. 查找时，会进行哈希到指定位置进行key值判断，不符合直接扫描下一个，删除也是如此
3. 删除后出现的一个问题：出现空槽，会被误以为搜索完成了，
	1. 设置标记：表示没有logic entry
	2. 数据移动：意识到有空槽,因为是圆形Buffer，导致逻辑和物理上的不一致，导致错误，且数据移动复杂
3. 可以预测需要的槽，实战中就是2n，n是我们要保存的key的数量
###### 非唯一键
1. 维护单独一个链表，使用链表存储键的值
2. 保存冗余的key：不断复制这个key。实战中主要使用
##### 罗宾汉哈希
1. 所在的位置与第一次进行hash所计算出位置间的距离差；尽量让每个key的位置靠近第一hash的位置
2. 距离相等则往下放，并更新counter为1，谁的数值大谁在原地，
3. 基于罗宾汉算法，需要进行条件检查，看能否将一个放到另一个位置上，会导致更多的写入，导致更多的缓存无效。所以在实战中线性探测哈希函数碾压一切
##### 布谷鸟哈希
1. 大多数人使用两张表，且为哈希函数提供一个种子，确保两次哈希的结果不同
2. 情况：都为空，随机选择；一个为空则选择另一个；都不为空，选择杀死一个，然后将杀死的放到到另一个表进行哈希，如果说被占领了，直接占用；再对被占用的进行哈希，放到空槽中
3. 可能会发生递归碰撞，也有可能碰撞到最初的元素。发生无限循环后，需要进行扩容
4. 使用这个哈希函数，需要取尽可能最小化递归碰撞所到来的影响
#### 动态哈希方案
##### 链式哈希
1. 为哈希表中的每个槽维护一个桶的链表，桶可以无限扩容；桶满了可以再分配一个新的桶
2. 通过将所有具有相同哈希键的元素放入同一个桶中来解决冲突。
3. 查找元素，哈希到对应的桶并线性搜索即可
4. 插入和删除简单
5. Java中默认的数据结构
##### 可扩展哈希
1. 全局Counter表示截取哈希值的前几位
2. 局部Counter只是为了让我们理解，实际上槽数组进行查找的时候并不需要这个
3. 查找通过槽数组找到对应的Page ID，
***将槽数组上的槽与所有的新的Page进行重新映射，代价会不会很高***
1. 它们依然保存在磁盘文件下中的同一个PageID下
2. 要做的就是更新槽数组所指向的实际数据的位置，操作是低价的，但移动代价高
***将整个Page存到slot数组还是Page Id***
1. PageID,每个桶就是一个页面
