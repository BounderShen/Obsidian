### HTML介绍

#### 开始学习HTML

##### 空元素
1. br：换行的意思
#### 属性
1. title:提示信息，当鼠标停留的时候
2. style：指定类型
3. lang: 声明为Web页面
4. 单双引号都可以：当包含双引号应使用单引号
#### Heading
1. style="font-size:60px"
#### paragraph
1. pre：里面写什么就是什么，保留空格和换行
#### styles
1. 可以对相关标题进行自定义:字体、背景、大小等等
##### Text Alignment
1. 文本对齐方式：center
2. 同一个属性有多个值时可以使用分号隔开
#### Formatting
1. b和strong都是以粗体显示
##### 链接
1. `<a href="xxx"></a>`

##### 块级元素和内联元素

1. 块级元素会自动换行开始
2. 内联元素

##### 添加元素

1. target：值为“_blank”将在新标签页中显示链接

##### 布尔属性

1. disabled：表示无法输入

##### HTML中的空白

1. HTML解释器会将连续出现的空白字符串减少为一个单独的空格字符

##### 特殊字符

1. <：&lt，>：&gt。
2. ’：&apos,"：&quot
3. &：&amp

##### 添加作者和描述

1. name：包含什么信息
2. content：实际内容
### 什么是Html<head>标签
##### 站点自定义标签
1. <link rel="icon" href="favicon.ico" type="image/x-icon">

### HTML基础

#### 斜体字、粗体字、下划线

1. <i>：外国文字、分类名称、技术术语、一种思想
2. <b>：关键字、产品名称、引导句
3. <u>：专有名词、拼写错误

### 建立超链接

#### URL和paht

1. 指向当前目录：`index.html`
2. 指向子目录：`href="projects/index.html"`
3. 指向上级目录：`../pdf/xx.pdf`

#### 文档片段

1. 链接到文档的特定部分
2. 给片段上ID
3. `href="contacts.html#Mailing_address"`
4. 同一个文件下：`href="#Mailing_address"`

