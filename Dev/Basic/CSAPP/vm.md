### VM概述
### VM系统
1. 如何得到PPN
#### address space
1. 线性地址空间使用的是非负整数
2. 虚拟地址空间大于物理地址空间
##### 为什么使用虚拟内存
1. 虚拟内存是存储在磁盘上的数据的DRAM缓存，提高主存效率
2. 简化内存管理
3. 隔离地址空间
	1. 一个进程不能访问、接触另一个的内存
	2. 用户程序不能访问内核和代码
#### VM as a tool for caching 
1. 虚拟内存的空间大多数是未分配的：通过动态地分配和释放内存，可以有效地减少内存的浪费，可以更好的满足进程的需求
2. 虚拟地址包含了所有可能需要的内存地址，包括进程代码、全局变量、堆、栈，但只有小部分实际上被分配到了物理地址
3. 当一个进程访问未分配的虚拟地址空间会发生
##### DRAM Cache Organization

#### Vm as a tool for memory management
#### VM as tool for memory protection
#### Address translation
