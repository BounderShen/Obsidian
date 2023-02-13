#### 连接操作
1. ssh -T git@github.com
2. git push 更新上github
3. 设置ssh key :ssh-keygen -t rsa -C "邮箱账号"
#### 配置工具
1. git config --global user.name ""
2. git config --global user.email ""
3. git config --global color.ui auto
##### 临时
###### git commit
1. 不加-m默认是写长篇注解，内容为则是取消
2. 格式
	1. 第一行：简述更改内容
	2. 第二行：空行
	3. 第三行：记述更改的原因和详细内容
###### git log
1. --all --graph --decorateo
2. git log 文件名
3. 
###### git checkout 
1. 后面提交一个哈希码（进行操作的）
2. 会改变当前的工作内容，再次执行会丢掉之前文件
###### git diff
1. 了解项目发生了什么？
2. 增加参数（快照码）
