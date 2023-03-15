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

#### For-Range结构

```go
for ix, value := range slice1 {
}
##value只是一个拷贝值无法进行修改
##可以忽略其中的一个值，使用空白符即可
```

##### 多维切片

```go
for row := range screen {
    for column := range screen[row] {
        screen[row][column] = 1
    }
}
```

#### 切片重组

1. 切片重组就是改变切片的长度
2. 切片后重组的长度和容量：`arr[5:6]`假设这个数组有10个长度，此时长度为6-5，cap是10-5

#### 切片的复制与追加

```go
slForm := []int{1,2,3}
slTo := make([]int,10)
##表示复制的多少个数字
n := copy(slTo,slForm)
##append会分配新的切片来保证已有切片元素和新增元素的存储，因此返回的切片可能指向一个不同的相关数组
slTo := append(slForm,4,5,6)
```

#### 字符串和数组和切片的应用

##### 字符串和切片的内存结构

1. 字符串是一个双字结构，指向实际数据的指针和记录字符串的长度的整数

##### 修改字符串中的某个字符

```go
s := "hello"
c := []byte(s)
c[0] = 'c'

```

##### append函数常见操作

1. `a = append(a,b...)`
2. 删除位于i的索引：`a = append(a[:i],a[:i+1])`
3. 切除切片a中索引i至j位置的元素：`a = append(a[:i],a[j:])`
4. 本质逻辑上就是：将append：里面的各种元素进行相加即可

##### 切片和垃圾回收

1. 切片的底层指向一个数组，该数组的实际容量可能要大于切片所定义的容量。只有在没有任何切片指向的时候，底层的数组内存才会被释放，这种特性有时会导致程序占用多余的内存

```go
var digitRegexp = regexp.MustCompile("[0-9]+")
func FindDigits(filename string) []byte {
    b, _ := ioutil.ReadFile(filename)
    return digitRegexp.Find(b)
}
####[]byte 指向的底层是整个文件的数据。只要该返回的切片不被释放，垃圾回收器就不能释放整个文件所占用的内存。换句话说，一点点有用的数据却占用了整个文件的内存
func FindDigits(filename string) []byte {
   b, _ := ioutil.ReadFile(filename)
   b = digitRegexp.Find(b)
   c := make([]byte, len(b))
   copy(c, b)
   return c
}
#### 找到所有数字
func FindFileDigits(filename string) []byte {
   fileBytes, _ := ioutil.ReadFile(filename)
   b := digitRegexp.FindAll(fileBytes, len(fileBytes))
   c := make([]byte, 0)
   for _, bytes := range b {
      c = append(c, bytes...)
   }
   return c
}
```

### Map

#### 声明和初始化和make

```go
var hashtable map[string]int
没有初始化的map是nil
key 可以是任意可以用 == 或者 != 操作符比较的类型 value 可以是任意类型的；通过使用空接口类型（详见第 11.9 节），我们可以存储任意值，但是使用这种类型作为值时需要先做一次类型断言（详见第 11.3 节）
map 传递给函数的代价很小：在 32 位机器上占 4 个字节，64 位机器上占 8 个字节
```

##### map容量

1. 当 map 增长到容量上限的时候，如果再增加新的 key-value 对，map 的大小会自动加 1。所以出于性能的考虑，对于大的 map 或者会快速扩张的 map，即使只是大概知道容量，也最好先标明
2. 可以设置初始容量

##### 用切片做map值

1. map1 := make[int] []int

##### 测试键值是否存在并删除

```go
_, ok := map1[key1] // 如果key1存在则ok == true，否则ok为false
delete(map1, "Washington")
```

##### for-range用法

```go
//可以使用空白符直接
for key, value := range map1 {
    ...
}
for key := range map1 {
    fmt.Printf("key is: %d\n", key)
}
```

##### map类型的切片

### 结构与方法

#### 结构体定义

```go
type myStruct struct {
    il int
    fl float32
    str string
}
var v myStruct    // v是结构体类型变量
var p *myStruct   // p是指向一个结构体类型变量的指针
//初始化时：可以指定进行赋值，也可以忽略，但不指定的，就需要按顺序进行赋值
```

##### 结构体布局

1. Go 语言中，结构体和它所包含的数据在内存中是以连续块的形式存在的，即使结构体中嵌套有其他的结构体，这在性能上带来了很大的优势

##### 结构体转换

1. 进行结构体转换时，不能直接用别名进行转换，需要使用原生的变量名进行转换

#### 使用工厂方法创建结构体实例

##### 结构体工厂

```go
type File struct {
    fd      int     // 文件描述符
    name    string  // 文件名
}
func NewFile(fd int, name string) *File {
    if fd < 0 {
        return nil
    }
    return &File{fd, name}
}
//查看结构体使用多少内存：size := unsafe.Sizeof(T)
```

##### 如何强制使用工厂方法

```go
type matrix struct {
    ...
}
func NewMatrix(params) *matrix {
    m := new(matrix) // 初始化 m
    return m
}
```

#### 使用自定义包中的结构体

1. ` struct1 := new(structPack.ExpStruct)`

#### 带标签的结构体

```go
package main
import (
    "fmt"
    "reflect"
)
type TagType struct { // tags
    field1 bool   "An important answer"
    field2 string "The name of the thing"
    field3 int    "How much there are"
}
func main() {
    tt := TagType{true, "Barak Obama", 1}
    for i := 0; i < 3; i++ {
        refTag(tt, i)
    }
}
func refTag(tt TagType, ix int) {
    //获取反射，通过Filed获取注释
    ttType := reflect.TypeOf(tt)
    ixField := ttType.Field(ix)
    fmt.Printf("%v\n", ixField.Tag)
}
```

#### 匿名字段和内嵌结构体

##### 定义

1. 结构体可以包含一个或多个 **匿名（或内嵌）字段**，即这些字段没有显式的名字，只有字段的类型是必须的，此时类型就是字段的名字。匿名字段本身可以是一个结构体类型，即 **结构体可以包含内嵌结构体**
2. Go 语言中的继承是通过内嵌或组合来实现的，
3. 在一个结构体中对于每一种数据类型只能有一个匿名字段

```go
package main
import "fmt"
type innerS struct {
    in1 int
    in2 int
}
type outerS struct {
    b    int
    c    float32
    int  // anonymous field
    innerS //anonymous field
}
func main() {
    outer := new(outerS)
    outer.b = 6
    outer.c = 7.5
    outer.int = 60
    outer.in1 = 5
    outer.in2 = 10
    fmt.Printf("outer.b is: %d\n", outer.b)
    fmt.Printf("outer.c is: %f\n", outer.c)
    fmt.Printf("outer.int is: %d\n", outer.int)
    fmt.Printf("outer.in1 is: %d\n", outer.in1)
    fmt.Printf("outer.in2 is: %d\n", outer.in2)
    // 使用结构体字面量
    outer2 := outerS{6, 7.5, 60, innerS{5, 10}}
    fmt.Println("outer2 is:", outer2)
}
```

##### 内嵌结构体

```go
package main
import "fmt"
type A struct {
    ax, ay int
}
type B struct {
    A
    bx, by float32
}
func main() {
    b := B{A{1, 2}, 3.0, 4.0}
    fmt.Println(b.ax, b.ay, b.bx, b.by)
    fmt.Println(b.A)
}
```

##### 命名冲突

1. 当两个字段拥有相同的名字时，外层名字会覆盖内层名字（但是两者的内存空间都保留），这提供了一种重载字段或方法的方式
2. 如果相同的名字在同一级别出现了两次，如果这个名字被程序使用了，将会引发一个错误（不使用没关系）。没有办法来解决这种问题引起的二义性，必须由程序员自己修正
3. `type D struct {B; b float32}`:想要内层的b可以通过d.B.b

#### 方法

##### 方法是什么

1. 接收者类型可以是（几乎）任何类型，不仅仅是结构体类型：任何类型都可以有方法，甚至可以是函数类型，可以是 int、bool、string 或数组的别名类型。接收者类型可以是（几乎）任何类型，不仅仅是结构体类型：任何类型都可以有方法，甚至可以是函数类型，可以是 int、bool、string 或数组的别名类型
2. 一个类型加上它的方法等价于面向对象中的一个类。一个重要的区别是：在 Go 中，类型的代码和绑定在它上面的方法的代码可以不放置在一起，它们可以存在在不同的源文件，唯一的要求是：它们必须是同一个包的
3. 如果基于接收者类型，是有重载的：具有同样名字的方法可以在 2 个或多个不同的接收者类型上存在，比如在同一个包里这么做是允许的
4. `func (a *denseMatrix) Add(b Matrix) Matrix`
5. `func (a *sparseMatrix) Add(b Matrix) Matrix`

```go
//本质上就是方法接收者，执行方法的人，可以使用自已的资源和传进来的参数进行操作
//
```

```go
package main
import "fmt"
type IntVector []int
func (v IntVector) Sum() (s int) {
    for _, x := range v {
        s += x
    }
    return
}
func main() {
    fmt.Println(IntVector{1, 2, 3}.Sum()) // 输出是6
}
```

### 读与数据

#### 读取用户的输入

```go
//Scanln 扫描来自标准输入的文本，将空格分隔的值依次存放到后续的参数内，直到碰到换行
fmt.Scanln(&firstName, &lastName)
//Sscan 和以 Sscan 开头的函数则是从字符串读取
fmt.Sscanf(input, format, &f, &i, &s)
//第二种方法
inputReader = bufio.NewReader(os.Stdin)
input,err = inputReader.ReadString("\n")
```

#### 文件读写

##### 读文件

```go
inputFile, inputError := os.Open("input.dat")
defer inputFile.Close()
inputReader := bufio.NewReader(inputFile)
inputString, readerError := inputReader.ReadString('\n')
```

##### 其他类似函数

```go
inputFile := "products.txt"
outputFile := "products_copy.txt"
buf, err := ioutil.ReadFile(inputFile)
err = ioutil.WriteFile(outputFile, buf, 0644)
```

##### 带缓冲的读取

```go
buf := make([]byte, 1024)
n, err := inputReader.Read(buf)
```

##### compress包：读取压缩文件

```go
package main
import (
    "fmt"
    "bufio"
    "os"
    "compress/gzip"
)
func main() {
    fName := "MyFile.gz"
    var r *bufio.Reader
    fi, err := os.Open(fName)
    if err != nil {
        fmt.Fprintf(os.Stderr, "%v, Can't open %s: error: %s\n", os.Args[0], fName,
            err)
        os.Exit(1)
    }
    defer fi.Close()
    fz, err := gzip.NewReader(fi)
    if err != nil {
        r = bufio.NewReader(fi)
    } else {
        r = bufio.NewReader(fz)
    }
    for {
        line, err := r.ReadString('\n')
        if err != nil {
            fmt.Println("Done reading file")
            os.Exit(0)
        }
        fmt.Println(line)
    }
}
```

##### 读文件

```go
package main
import (
    "os"
    "bufio"
    "fmt"
)
func main () {
    // var outputWriter *bufio.Writer
    // var outputFile *os.File
    // var outputError os.Error
    // var outputString string
    outputFile, outputError := os.OpenFile("output.dat", os.O_WRONLY|os.O_CREATE, 0666)
    if outputError != nil {
        fmt.Printf("An error occurred with file opening or creation\n")
        return  
    }
    defer outputFile.Close()
    outputWriter := bufio.NewWriter(outputFile)
    outputString := "hello world!\n"
    for i:=0; i<10; i++ {
        outputWriter.WriteString(outputString)
    }
    outputWriter.Flush()
}
//直接写入文件
fmt.Fprintf(outputFile, "Some test data.\n")
//直接输入到屏幕上
os.Stdout.WriteString("hello, world\n")
```

#### 文件拷贝

```go
// filecopy.go
package main
import (
    "fmt"
    "io"
    "os"
)
func main() {
    CopyFile("target.txt", "source.txt")
    fmt.Println("Copy done!")
}
func CopyFile(dstName, srcName string) (written int64, err error) {
    src, err := os.Open(srcName)
    if err != nil {
        return
    }
    defer src.Close()
    dst, err := os.Create(dstName)
    if err != nil {
        return
    }
    defer dst.Close()
    return io.Copy(dst, src)
}
// 打开文件，创建文件，使用io.Copy函数并传入打开文件的变量和创建文件的变量
```

#### 从命令行读取参数

##### os包

```go
// os_args.go
package main
import (
    "fmt"
    "os"
    "strings"
)
func main() {
    who := "Alice "
    if len(os.Args) > 1 {
        who += strings.Join(os.Args[1:], " ")
    }
    fmt.Println("Good Morning", who)
}
```

##### flag包

```go
package main
import (
    "flag" // command line option parser
    "os"
)
var NewLine = flag.Bool("n", false, "print newline") // echo -n flag, of type *bool
const (
    Space   = " "
    Newline = "\n"
)
func main() {
    //打印帮助信息
    flag.PrintDefaults()
    flag.Parse() // Scans the arg list and sets up flags
    var s string = ""
    for i := 0; i < flag.NArg(); i++ {
        if i > 0 {
            s += " "
            if *NewLine { // -n is parsed, flag becomes true
                s += Newline
            }
        }
        s += flag.Arg(i)
    }
    os.Stdout.WriteString(s)
}
/**
flag.Parse() 扫描参数列表（或者常量列表）并设置 flag, flag.Arg(i) 表示第i个参数。Parse() 之后 flag.Arg(i) 全部可用，flag.Arg(0) 就是第一个真实的 flag，而不是像 os.Args(0) 放置程序的名字。

flag.Narg() 返回参数的数量。解析后 flag 或常量就可用了。 flag.Bool() 定义了一个默认值是 false 的 flag：当在命令行出现了第一个参数（这里是 “n”），flag 被设置成 true（NewLine 是 *bool 类型）。flag 被解引用到 *NewLine，所以当值是 true 时将添加一个 Newline（”\n”）。
*/

```

##### 用buffer读取文件

```go
package main
import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "os"
)
func cat(r *bufio.Reader) {
    for {
        buf, err := r.ReadBytes('\n')
        fmt.Fprintf(os.Stdout, "%s", buf)
        if err == io.EOF {
            break
        }
    }
    return
}
func main() {
    flag.Parse()
    if flag.NArg() == 0 {
        cat(bufio.NewReader(os.Stdin))
    }
    for i := 0; i < flag.NArg(); i++ {
        f, err := os.Open(flag.Arg(i))
        if err != nil {
            fmt.Fprintf(os.Stderr, "%s:error reading from %s: %s\n", os.Args[0], flag.Arg(i), err.Error())
            continue
        }
        cat(bufio.NewReader(f))
        f.Close()
    }
}
```

#### 用切片读写文件

```go
func cat(f *os.File) {
    const NBUF = 512
    var buf [NBUF]byte
    for {
        switch nr, err := f.Read(buf[:]);  {
        case nr < 0:
            fmt.Fprintf(os.Stderr, "cat: error reading: %s\n", err.Error())
            os.Exit(1)
        case nr == 0: // EOF
            return
        case nr > 0:
            if nw, ew := os.Stdout.Write(buf[0:nr]); nw != nr {
                fmt.Fprintf(os.Stderr, "cat: error writing: %s\n", ew.Error())
            }
        }
    }
}
```

```go
package main
import (
    "flag"
    "fmt"
    "os"
)
func cat(f *os.File) {
    const NBUF = 512
    var buf [NBUF]byte
    for {
        switch nr, err := f.Read(buf[:]); true {
        case nr < 0:
            fmt.Fprintf(os.Stderr, "cat: error reading: %s\n", err.Error())
            os.Exit(1)
        case nr == 0: // EOF
            return
        case nr > 0:
            if nw, ew := os.Stdout.Write(buf[0:nr]); nw != nr {
                fmt.Fprintf(os.Stderr, "cat: error writing: %s\n", ew.Error())
            }
        }
    }
}
func main() {
    flag.Parse() // Scans the arg list and sets up flags
    if flag.NArg() == 0 {
        cat(os.Stdin)
    }
    for i := 0; i < flag.NArg(); i++ {
        f, err := os.Open(flag.Arg(i))
        if f == nil {
            fmt.Fprintf(os.Stderr, "cat: can't open %s: error %s\n", flag.Arg(i), err)
            os.Exit(1)
        }
        cat(f)
        f.Close()
    }
}
```

#### 使用接口的实际例子：fmt.Printf

```go
// interfaces being used in the GO-package fmt
package main
import (
    "bufio"
    "fmt"
    "os"
)
func main() {
    // unbuffered
    fmt.Fprintf(os.Stdout, "%s\n", "hello world! - unbuffered")
    // buffered: os.Stdout implements io.Writer
    buf := bufio.NewWriter(os.Stdout)
    // and now so does buf.
    fmt.Fprintf(buf, "%s\n", "hello world! - buffered")
    buf.Flush()
}
```

