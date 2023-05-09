##### 表索引
1. 表索引就是我们表中属性的子集的副本
2. 对于每个数据库创建的索引平衡：存储开销、维护开销
#### B+Treee
##### B+树
1. Post gres实际上使用的是B+树
2. 自平衡树（log n），保持数据是有顺序的，顺序访问、增删改始终是log n
4. 对系统进行读写大块数据优化
##### B+树属性
1. 多路查找树且是完美平衡：每个节点可以通过M条路线到达其他节点
3. 节点不处于半满的状态，将周围的数据移动过去，让它变成半满状态，这是维持log n的方法
##### 节点
1. 每一个B+树节点由一个键/值对数组组成
2. 键是基于索引基础属性而派生出来的。
3. 值将根据节点是被分类为内部节点还是叶节点而有所不同。
##### B+树叶子节点
1. 从页面逻辑，不管你key数组中的offset值是什么，它始终对应了value数组中的某些 offset值
##### 叶子节点值
1. Record IDS ：指向与索引条目对应元组位置的指针。Postgre,也是所有数据库常用的做法
2. 索引遍历，拿到Record ID,在Page表中根据记录ID找到想要，跑到块进行扫描
3. 元组数据：叶节点存储元组的实际内容。次级索引必须将记录ID存储为其值。商用，Oracle和sql server默认情况1
##### B树 VS B+树
1. value值可以放在任何一个位置且只出现一次，使用空间少
2. 我会将所有的路标都放在inner node中，当我将它从叶⼦节点上删除时，我可能会将它保存在inner node中，因为如果我要查找其他key，那么我还可以通过这条路线往下去查找
3. B树多线程操作情况下进行更新操作代价昂贵，例如：我有⼀个inner node，我对它进⾏某些修改。然后，我将这个修改向上和向下进⾏传播(知秋注：修改删除某⼀个inner node所带来的影响， ⽐如它内部数据结构中相关指针的指向，这个在并发操作下是需要保护的）我必须在这两个⽅向上加⼀个latch
4. B+树只需要对一个方向加latch
##### B+树插入
1. 找到正确的叶节点 L。将数据条目按顺序插入 L。如果 L 有足够的空间，完成！
2. 否则，将 L 键拆分为 L 和一个新节点 L2。重新分配条目，复制中间键。将指向 L2 的索引条目插入 L 的父节点。要拆分内部节点，需要均匀地重新分配条目，但是需要把中间键推到上面。
3. 不要在不适用东西上加索引
4. 主键要唯一
##### B+树删除
1. 从根节点开始，找到条目所属的叶节点 L。删除该条目。如果 L 至少有一半的空间，完成！
2. 如果 L 只有 M/2-1 条目，尝试从兄弟节点（与 L 具有相同父节点的相邻节点）借用重新分配。如果重新分配失败，将 L 和兄弟节点合并。如果发生合并，则必须从 L 的父节点删除指向 L 或兄弟节点的条目。
##### 实战中的B+树
1. 填充因子：67%
2. 典型容量：
	1. Height:4, 1334 = 312900721
	2. Height:3 1333 = 2406,104
3. 页数级别
	1. 级别1：1page = 8KB
	2. 级别2：134page = 1MB
	3. 级别3：17956 pages = 140MB
##### 聚簇索引
1. 因为插入表中的数据排序是无序的
2. 按主键排列->聚簇索引
3. 数据库系统会保证，索引会对page中tuple的物理布局进⾏匹配排序（知秋注：对磁盘上实际 数据重新组织以按指定的⼀个或多个列的值排序）
4. 
#### 设计决策
#### 优化