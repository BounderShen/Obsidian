### vs code下安装go扩展失败

1. CMD下执行

2. ```javascript
   go ``env` `-w GO111MODULE=on
   go env -w GOPROXY=https://goproxy.io,direct
   ```

#### 如何go是如何运行的

1. go build 编译源码
2. go run 编译执行文件
3. go fmt 
4. go install 编译和安装package
5. go get 下载源码包
6. go test 运行

#### package

1. 相当于工作空间或者项目

2. 两个包类型：

   1. 执行包：main
   2. 重用：相当于依
   ### 程序结构

   1. 字符串类型对应的零值是空字符串，接口或引用类型（包括slice、指针、map、chan和函数）变量对应的零值是nil。数组或结构体等聚合类型对应的零值是每个元素或字段都是对应该类型的零值
   2. 任何类型的指针的零值都是nil
#### 赋值
##### 元组赋值
1. `x,y = y, x%y`
2. map查找失败时会返回零值
3. type断言，失败时返回panic异常
4. 管道接受时，失败时返回零值
#### 可赋值性

1. `medals := []string{"gold","silver","bronze"}`

#### 类型

1. `type 类型名字 底层类型`
### 包和文件
#### 包的初始化
1. 解决包级变量的依赖顺序，然后按照变量的声明顺序依次初始化
2. 包中含有go文件，Go语言构建工具会根据文件名进行排序，然后依次调用编译器编译
3. 使用初始化函数
4. 初始化函数不能被调用和引用
5. 每个包在解决依赖的前提下。以导入声明的顺序初始化，每个包只会被初始化一次。初始化工作是自下而上进行，确保所有的包被加载，再到main包
#### 作用域
1. 声明语句是一个编译时期，生命周期是运行时
2. 当编译器遇到一个名字引用时，它会对其定义进行查找，查找过程从内层的词法域向全局的作用域进行
### 数据类型
#### 整型
1. byte等价于unit8，byte强调的是数值是一个原始的数据而不是一个小的整数
2. uintptr：没有指定具体的bit大小但是可以容纳指针
#### 浮点数
1. float32类型的浮点数只能提供6个十进制的精度，而float64可以提供15个
2. 因为float类型的累计计算误差很容易扩散，并且float能精确表示的正整数不是很大，有效位整数只有23个，超过将会表示误差

#### Slice
1. for index xxx := range yyy
## Go入门指南
### 基本结构和基本数据类型
#### 包的概念、导入与可见性
   1. 如果对一个包进行更改或重新编译，所有引用了这个包的客户端程序都必须全部重新编译
   2. 每一段代码只会被编译一次
##### 可见性规则
1. 当标识符（常量、变量、类型、函数名、结构字段等）以大写字母开头，那么就会被外部包的代码所用；以小写只能被包内部可用
##### Go程序的执行顺序
1. main包导入其他包，则递归导包
2. 1.  然后以相反的顺序在每个包中初始化常量和变量，如果该包含有 init 函数的话，则调用该函数。
3. 在完成这一切之后，main 也执行同样的过程，最后调用 main 函数开始执行程序
#### 常量
1. 只可以是布尔型、数字型和字符型
2. 数字型的常量是没有大小和符号的，并且可以使用任何精度而不会导致溢出
3. iota：第一个默认值是0，在新的一行被使用的时候会自动加1
4. 同一行赋值两个常量不会递增
5. 赋值以常量时，之后没赋值会应用上一行的表达式
#### 变量
##### init函数
1. 一个源文件都只能包含一个 init 函数。初始化总是以单线程执行，并且按照包的依赖关系顺序执行
#### 基本类型和运算符
##### 布尔类型
1. %t
##### 数字类型
###### 整型int和浮点型float
1. float32精确到32位，float64精确到15位
2. 前缀 0 来表示 8 进制数（如：077），增加前缀 0x 来表示 16 进制数（如：0xFF），以及使用 e 来表示 10 的连乘（如： 1e3 = 1000，或者 6.022e23 = 6.022 x 1e23）
3. 在格式化字符串里，`%d` 用于格式化整数（`%x` 和 `%X` 用于格式化 16 进制表示的数字），`%g` 用于格式化浮点型（`%f` 输出浮点数，`%e` 输出科学计数表示法），`%0nd` 用于规定输出长度为n的整数，其中开头的数字 0 是必须的。
##### 复数
1. %v:输出所有的值，%+v：输出字段和值，%#v：输出所有信息
2. 函数 `real(c)` 和 `imag(c)` 可以分别获得相应的实数和虚数部分
##### 位运算
1. %b：用于表示位的格式化标识符
2. 异或：无进位相加
##### 算术运算符
1. 自增自减只能作为一个语句
##### 随机数
1. rand.float32返回的是：(0到1之间）
##### 运算符优先级
1. 1.  `优先级 运算符`
2.  `7 ^ !`
3.  `6 * / % << >> & &^`
4.  `5 + - | ^`
5.  `4 == != < <= >= >`
6.  `3 <-`
7.  `2 &&`
8.  `1 ||`
##### 字符类型
1. 在书写 Unicode 字符时，需要在 16 进制数之前加上前缀 `\u` 或者 `\U`
2. 前缀 `\u` 则总是紧跟着长度为 4 的 16 进制数，前缀 `\U` 紧跟着长度为 8 的 16 进制数
3. 格式化说明符 `%c` 用于表示字符；当和字符配合使用时，`%v` 或 `%d` 会输出用于表示该字符的整数；`%U` 输出格式为 U+hhhh 的字符串
#####字符串
1. 使用反引号括起来会远洋输出
2. 使用strings.join进行拼接字符
#### strings+strconv包
##### 前缀和后缀
1. strings.HasPrefix(s,prefix) bool
##### 字符串包含关系
1. strings.Contains(s,substr string) bool
##### 判断字符串或字符在父字符串中出现的位置（索引）
1. strings.Index(s,str string) int :返回-1表示不存在
2. string.LastIndex(s,str string) int :返回子字符串出现在字符中的位置
##### 字符串替换
1. strings.Replace(str,old,new, n) string
2. n：表示替换前几个，-1表示替换全部
##### 统计字符串出现次数
1. strings.Count(s,str string) int
##### 重复字符串
1. strings.Repeat(s, count int) string
2. 重复这个字符串多少次，然后返回新的
##### 修改字符串大小
1. strings.ToLower(s) string
2. strings.ToUpper(s) string
##### 修剪字符
1. strings.TrimSpace(s):去除字符串开头或者结尾的空白符号
2. string.Trim(s,"cut"):去掉开头和结尾的cut
3. string.TrimLeft/Right：去除左或者右
##### 分割字符串
1. strings.Fields(s):将会利用1个或多个空白字符来作为动态长度的额分割字符将字符串分割成若干小块，并返回slice，如果字符串只包含空白符号，则返回一个长度为 0 的 slice
2. `strings.Split(s, sep)` 用于自定义分割符号来对指定字符串进行分割，同样返回 slice
##### 拼接slice到字符串
1. strings.join(sl []string,sep string)
##### 从字符串中读取内容
1. strings.NewReader(str):生成一个reader并获取字符串中的内容并返回该指针
2. Read：从[]byte
3. ReadByte 和 readRune
##### 字符串与其他类型转换
1. 通过strconv
2. `strconv.Itoa(i int) string` 返回数字 i 所表示的字符串类型的十进制数
3. `strconv.FormatFloat(f float64, fmt byte, prec int, bitSize int) string` 将 64 位浮点型的数字转换为字符串，其中 `fmt` 表示格式（其值可以是 `'b'`、`'e'`、`'f'` 或 `'g'`），`prec` 表示精度，`bitSize` 则使用 32 表示 float32，用 64 表示 float64
4. `strconv.Atoi(s string) (i int, err error)` 将字符串转换为 int 型
5. `strconv.ParseFloat(s string, bitSize int) (f float64, err error)` 将字符串转换为 float64 型
#### 时间和日期
1. duration：两个时间相差的纳秒数，类型为int64
2. time.Day():以此类推
3. time.add（“纳秒”：比如一周给为 60 * 60 * 7 *24 * 1e9 ）
4. time.Now().UTC（）
#### 指针
1. Go 语言的取地址符是 `&`，放到一个变量前使用就会返回相应变量的内存地址
2. **一个指针变量可以指向任何一个值的内存地址** 它指向那个值的内存地址，在 32 位机器上占用 4 个字节，在 64 位机器上占用 8 个字节，并且与它所指向的值的大小无关
3. 由于经常导致 C 语言内存泄漏继而程序崩溃的指针运算（所谓的指针算法，如：`pointer+2`，移动指针指向字符串的字节数或数组的某个位置）是不被允许的
### 控制结构
#### if else 结构
1. **注意事项** 不要同时在 if-else 结构的两个分支里都使用 return 语句，这将导致编译报错 `function ends without a return statement`（你可以认为这是一个编译器的 Bug 或者特性）。（ **译者注：该问题已经在 Go 1.1 中被修复或者说改进** ）
#### 测试多返回值函数的错误
1. Go 语言的函数经常使用两个返回值来表示执行是否成功：返回某个值以及 true 表示成功；返回零值（或 nil）和 false 表示失败。可以用 error 类型的变量来代替作为第二个返回值：成功执行的话，error 的值为 nil，否则就会包含相应的错误信息
2. 习惯用法： `if err != nil {fmt.Printf("Program stopping with error %v",err)} os.Exit(1)` 

#### switch结构

1. 变量 var1 可以是任何类型，而 val1 和 val2 则可以是同类型的任意值。类型不被局限于常量或整数，但必须是相同的类型；或者最终结果为相同类型的表达式
2. 您可以同时测试多个可能符合条件的值，使用逗号分割它们
3. 每一个 `case` 分支都是唯一的，从上至下逐一测试，直到匹配为止。（ Go 语言使用快速的查找算法来测试 switch 条件与 case 分支的匹配情况，直到算法匹配到某个 case 或者进入 default 条件为止。
4. 一旦成功地匹配到某个分支，在执行完相应代码后就会退出整个 switch 代码块，也就是说您不需要特别使用 `break` 语句来表示结束
5. 使用fallthrough：继续执行后续分支的代码
6. 同样可以使用 `return` 语句来提前结束代码块的执行。当您在 switch 语句块中使用 `return` 语句，并且您的函数是有返回值的，您还需要在 switch 之后添加相应的 `return` 语句以确保函数始终会返回

##### 第一种类型

```go
switch num1 {
	case 98,99:
		fmt.Println("It is euqal to 98")
	case 100:
		fmt.Println("It's equal to 100")
	default:
		fmt.Println("It's not equal to 98 or 99")
	}

```

##### 第二种类型

```go
switch {
	case num1 < 0:
		fmt.Println("Number is negative")
	case num1 > 0 && num1 <10:
		fmt.Println("Number is between 0 and 10")
	default:
		fmt.Println("Number is 10 or greater")
	}
```

##### 第三种类型:到初始化语句

```go
switch result := calculate(); {
    case result < 0:
        ...
    case result > 0:
        ...
    default:
        // 0
}
switch a, b := x[i], y[j]; {
    case a < b: t = -1
    case a == b: t = 0
    case a > b: t = 1
}
```

#### for结构

##### 无限循环

1. 条件语句是可以被省略的，如 `i:=0; ; i++` 或 `for { }` 或 `for ;; { }`（`;;` 会在使用 gofmt 时被移除）：这些循环的本质就是无限循环。最后一个形式也可以被改写为 `for true { }`，但一般情况下都会直接写 `for { }`

##### for-range结构

1. 一般形式为：`for ix, val := range coll { }`
2. 要注意的是，`val` 始终为集合中对应索引的值拷贝，因此它一般只具有只读性质，对它所做的任何修改都不会影响到集合中原有的值（**译者注：如果 `val` 为指针，则会产生指针的拷贝，依旧可以修改集合中的原值**）

##### 标签与goto

1. 不建议使用标签与goto
2. 非要使用标签语句要在goto后面

### 函数

#### 介绍

1. Go 语言不支持这项特性的主要原因是函数重载需要进行多余的类型匹配影响性能
2. ***函数值（functions value）之间可以相互比较：如果它们引用的是相同的函数或者都是 nil 的话，则认为它们是相同的函数。函数不能在其它函数里面声明（不能嵌套），不过我们可以通过使用匿名函数（参考 [第 6.8 节](https://www.bookstack.cn/read/the-way-to-go_ZH_CN/eBook-06.8.md)）来破除这个限制***

#### 函数与返回值

1. 事实上，任何一个有返回值（单个或多个）的函数都必须以 `return` 或 `panic`（参考 [第 13 章](https://www.bookstack.cn/read/the-way-to-go_ZH_CN/eBook-13.0.md)）结尾

##### 按值传递和按引用传递

1. Go 默认使用按值传递来传递参数，也就是传递参数的副本
2. **指针也是变量类型，有自己的地址和值，通常指针的值指向一个变量的地址。所以，按引用传递也是按值传递**
3. 如果一个函数需要返回四到五个值，我们可以传递一个切片给函数（如果返回值具有相同类型）或者是传递一个结构体（如果返回值具有不同的类型）。因为传递一个指针允许直接修改变量的值，消耗也更少

##### 命名的返回值

1. return：直接默认返回所有，但执行函数声明时需要写出详细的返回类型和命名，
2. 推荐使用命名式

```go

```

##### 空白符

1. 使用自动忽略返回值
2. 改变外部变量需要传入指针地址

#### 传递变长参数

1. `func Greeting(prefix string, who ...string)`
2. 个接受变长参数的函数可以将这个参数作为其它函数的参数进行传递
#### defer和追踪
1. 延迟语句的执行，知道当前函数Return返回之后才执行
#### 内置函数
#### 递归函数
1. 出现在大量的递归调用导致的程序栈内存分配耗尽
#### 将函数作为参数
1. 直接传入函数名即可
#### 匿名函数
1. 不能单独存在，但可以赋值给变量
2. 在函数的右括号需要加入一对圆括号表明是匿名函数
### 数组与切片
#### 声明和初始化
1. `var arr [5]int`
2. 传入数组名是直接复制值过去，而&arr是直接将地址传递过去，可以进行修改
3. 知道值赋值：`var arr [10]int{}`
4. 使用key和value值：`var arrKeyValue = [8]int{3 : "Chris",4 : "Go"}`
#### 切片
##### 概念
1. `var arr []int`
2. 初始化格式：`var arr []int = arr1[start:end]`,start和end不写这是整个数组复制过去，也可以采用地址的方法赋值过去
3. 切片在内存中组织的方式是一个有3个域的结构体：指向相关的数组指针，切片长度以及切片容量
##### make创建切片
1. `make([]int,len,cap)`:cap参数可以忽略
##### new()和make()的区别
1. 都在堆上分配内存
2. new(T) 为每个新的类型T分配一片内存，初始化为 0 并且返回类型为*T的内存地址：这种方法 **返回一个指向类型为 T，值为 0 的地址的指针**，它适用于值类型如数组和结构体（参见第 10 章）；它相当于 `&T{}`
3. make(T) **返回一个类型为 T 的初始值**，它只适用于3种内建的引用类型：切片、map 和 channel
##### bytes包
1. `var buffer bytes.Buffer`
2. `var r *bytes.Buffer` = new(bytes.Buffer)
3. 通过buffer串联字符：`buffer.WriteString(s) buffer.String()`
4. 