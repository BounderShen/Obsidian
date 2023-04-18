#### 常用命令
##### mv命令
1. mv 文件名 文件名：修改的是第一个文件的名字
2. mv 文件名 文件名 文件名 文件目录：移动多个文件到指定目录
##### cp命令
1. cp fileName fileDir：复制文件到指定目录
2. cp -a 文件目录 文件目录：复制文件到指定目录
##### cat
1. 查看：
2. cat -n ：加行号显示
##### more
1. ```more +3 filename
2. ``` more +/day3 test.log
3. more -5 filename
##### less
1. less filename
##### head
1. ```head -n 5 filename```
##### tail
1. tail -n 5 test.txt
2. tail -f test.txt
#### 文件查找
##### which命令
1. which more
##### whereis 
whereis命令是定位可执行文件、源代码文件、帮助文件在文件系统中的位置
1. whereis xxx
2. whereis -b xxx