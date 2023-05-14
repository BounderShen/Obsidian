#### 初步安装
1. 官方下载iso，可以使用下方的镜像源下载
2. 虚拟机安装注意点将磁盘文件作为一个单文件，而不是分为多个
3. 在虚拟机界面编辑，选择选项，再到高级处UEFI
4. 启动虚拟机`ls /sys/firmware/efi/efivars`没有报错就是UEFI模式引导的
5. 使用ping来`ping www.baidu.com`
6. 执行命令获取ip`ip -brief address`
7. 修改密码`passwd`
##### 更换国内镜像源
1. `pacman -Sy vim`
2. 使用`vim /etc/pacman.d/mirrorlist`,在上面配置`Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch`
##### 磁盘分区
1. `fdisk -l`
2. `cfdisk /dev/sda`,选择gpt
3. 选择new回车：300MB，选择类型：EFI system回车
4. 切到Free space，选择new分区，swap分区：4G，Type：Linux Swap。root默认分配剩余空间，默认文件系统
5. 分区后选择`write`有提示就输入yes回车，然后退出
##### 问题安装ysy出现问题
1. 主要问题是前面没有配置`vim /etc/pacman.conf`:在里面添加`[archlinuxcn] SigLevel = Optional TrustAll Server = https://repo.archlinuxcn.org/arch`
2. `pacman -Sy`
3. `pacman archlinuxcn-keyring`
4. 