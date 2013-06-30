PyAutoUpdateSmartHosts
======================

Update my hosts to the latest version of smart hosts automatically

本脚本目前支持Windows系统下Hosts文件的更新，可以只能识别出你的hosts文件里的SmartHosts部分（现在还有个前提，就是你的hosts文件里不能有第二个像#UPDATE:XXXX-XX-XX XX:XX这样的标记，将来我会考虑解决的），然后将你的hosts与最新版比较并进行更新。更新前会自动设置备份。

###目前已知问题：

 - 对受系统读写保护Hosts无法更新(Linux)

 - ~~不支持Linux系统~~

 - ~~无境内版和境外版的选择选项~~

 - hosts文件里不能有第二个像#UPDATE:XXXX-XX-XX XX:XX这样的标记

 - 不能自动清理生产的cache文件夹

 - ~~无法处理用户Windows系统未安装在C盘或当前Windows系统目录不在C盘的情况~~


###使用方法：

本脚本在Python2.7和Python3.2下测试通过，运行时需要安装第三方库httplib2。
如果你的电脑没有Python环境，我用pyInstaller打包了一个exe文件，下载地址：(http://pan.baidu.com/share/link?shareid=474827113&uk=1445599042)
