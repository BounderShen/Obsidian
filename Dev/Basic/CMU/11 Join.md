#### 前言
##### 为什么我们需要Join
1. 在没有任何信息丢失的情况下，join operator允许我们去对原来的tuple进⾏重组
2. inner equijoin这种对两表进⾏join的算法，是⽬前数据库系统中最常⻅实现的算法
3. 这也是每个主流的开源数据库系统和商⽤数据库系统所做的事情
4. 当然也有能够进⾏M-way join的算法，它可以在同⼀时间对三张或更多张表进⾏join操作。高端的数据库也支持这些了。
##### 操作输出
1. 处理模型
2. 存储模型
3. 哪种查询
4. 列式还是行式存储
5. 然后根据record id或者tuple id中的page number 以及offset值，我们可以找到我们数据库中 该tuple⾥的其余数据
##### 延迟操作
1. 如果我们可以尽可能延迟进⾏这种⽣成操作，该⽣成操作会把所有的列数据变回tuple原 本的形式（列变⾏，tuple代表⼀⾏数据）（11-01，9.45）
2. late materialization
##### 如何判断Join算法
1. 根据IO次数的成本来判断
#### 嵌套循环
##### 成本分析
1. M + （m ** N）
##### block
1. 让内外表各用一个块，对于outer table所⽤的每个block⽽⾔，我们每次会从inner table中拿到⼀个block
2. 我们会让outer table block中的每个tuple和inner table block中的所有tuple进⾏join
3. 直到我们完成了对outer table block中所有tuple的join操作，我们才会和inner table中下⼀个 block中的所有tuple进⾏join
4. outer table 是更小的表