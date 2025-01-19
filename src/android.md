---
# Android
---

# 常见的root工具

* [kingRoot](https://root-apk.kingoapp.com/)

* [root master](https://root-master.com/)

* [lineageos-第三方系统](https://www.lineageos.org/)

* [airtest-网易的自动化测试框架](https://airtest.doc.io.netease.com/)

## [adb](https://developer.android.google.cn/tools/adb?hl=zh-cn)

* 客户端：用于发送命令。客户端在开发机器上运行。您可以通过发出 adb 命令从命令行终端调用客户端。
* 守护程序 (adbd)：用于在设备上运行命令。守护程序在每个设备上作为后台进程运行。
* 服务器：用于管理客户端与守护程序之间的通信。服务器在开发机器上作为后台进程运行。

## UI Automator

UI Automator是由谷歌开发和维护的移动测试Android UI框架，它的主要功能包含了跨应用程序的功能测试，即测试多个应用程序和在已安装与系统应用程序之间的切换的功能。

UI Automator是一个黑盒测试工具，也就是说测试开发人员不需要知道内部的应用程序结构，可以完全依赖于可见的UI元素。UI Automator的测试是用Java编写的，由两组api组成：其一为UI Automator APIs，是控制应用程序的UI组件；其二为device state APIs，用于访问和执行设备上的操作（如改变设备旋转，按方向键按钮，按返回，Home或者菜单按钮等）。它还附带了一个非常有用的UI Automator Viewer，这是一个可以扫描和分析当前配置在设备上的UI组件的图形用户界面工具。

UI Automator的缺点是不支持构建在混合Android应用程序之上的WebView，因此，UI Automator只支持原生的Android应用程序。
