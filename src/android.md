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

在Android设备中，**Recovery** 是一个独立的、轻量级的操作系统环境，专门用于系统维护和恢复操作。它独立于主操作系统（Android系统），允许用户在设备无法正常启动时进行故障排除、数据恢复或系统更新。

## Recovery 的主要功能

1. **系统恢复**：
   * 恢复设备到出厂设置。
   * 修复系统问题（如系统崩溃或无法启动）。

2. **系统更新**：
   * 安装官方OTA（Over-The-Air）更新。
   * 手动刷入官方或第三方ROM。

3. **数据管理**：
   * 清除缓存、用户数据或整个系统分区。
   * 备份和恢复系统（如Nandroid备份）。

4. **高级操作**：
   * 刷入第三方ROM、Kernel、Modem等。
   * 获取Root权限或安装Magisk。

---

### Recovery 的类型

1. **Stock Recovery（官方Recovery）**：
   * 由设备制造商提供，功能有限。
   * 通常只支持官方OTA更新和恢复出厂设置。
   * 不支持刷入第三方ROM或自定义操作。

2. **Custom Recovery（第三方Recovery）**：
   * 由开发者社区创建，功能强大。
   * 常见的有 **TWRP（Team Win Recovery Project）** 和 **ClockworkMod（CWM）**。
   * 支持刷入第三方ROM、备份和恢复系统、挂载分区等高级功能。

---

### Recovery 的常见操作

1. **进入Recovery模式**：
   * 通常通过组合键（如 **音量上 + 电源键**）进入。
   * 也可以通过ADB命令进入：

     ```bash
     adb reboot recovery
     ```

2. **Wipe（清除数据）**：
   * **Wipe Data/Factory Reset**：清除用户数据，恢复出厂设置。
   * **Wipe Cache Partition**：清除缓存分区，解决系统卡顿或更新问题。
   * **Advanced Wipe**：选择清除特定分区（如System、Data、Cache等）。

3. **Install（安装）**：
   * 刷入ZIP文件，如ROM、GApps、Kernel、Magisk等。
   * 在TWRP中，选择“Install”并选择ZIP文件即可。

4. **Backup（备份）**：
   * 创建Nandroid备份，完整备份系统、数据、缓存等。
   * 备份文件通常存储在设备的内部存储或SD卡中。

5. **Restore（恢复）**：
   * 从Nandroid备份中恢复系统。
   * 用于修复系统问题或回滚到之前的系统状态。

6. **Mount（挂载分区）**：
   * 挂载系统分区、数据分区等，便于访问或修改文件。
   * 在TWRP中，可以通过“Mount”选项启用或禁用分区挂载。

7. **Advanced（高级功能）**：
   * **File Manager**：管理设备文件。
   * **ADB Sideload**：通过ADB从电脑推送文件并刷入。
   * **Terminal**：使用命令行执行操作。

---

### Recovery 的作用场景

1. **系统崩溃或无法启动**：
   * 通过Recovery恢复备份或清除数据。

2. **刷机**：
   * 刷入第三方ROM、Kernel或Modem。

3. **Root权限**：
   * 通过Recovery刷入Magisk或SuperSU获取Root权限。

4. **系统优化**：
   * 清除缓存分区以提升性能。
   * 刷入优化脚本或模块。

---

### 总结

Recovery 是Android设备中一个强大的工具，用于系统维护、恢复和刷机操作。官方Recovery功能有限，而第三方Recovery（如TWRP）提供了更多高级功能，适合喜欢折腾设备的用户。无论是修复系统问题还是刷入自定义ROM，Recovery都是不可或缺的工具。

## ROM介绍

Android系统的ROM（Read-Only Memory）是一个包含操作系统、应用程序和系统配置的文件集合。它通常以ZIP格式打包，刷入设备后成为设备的操作系统。以下是ROM中常见的文件和文件夹及其作用：

---

### 1. **系统核心文件**

这些文件是Android系统运行的基础，通常位于ROM的根目录或`system`分区中。

* **`system.img` 或 `system/` 文件夹**：
  * 包含Android系统的核心文件，如系统应用、库文件、配置文件等。
  * 刷机时会将`system.img`或`system/`文件夹解压并写入设备的`system`分区。

* **`boot.img`**：
  * 包含内核（Kernel）和初始内存磁盘（RAMDisk），负责启动设备并加载系统。
  * 刷机时会将`boot.img`写入设备的`boot`分区。

* **`vendor.img` 或 `vendor/` 文件夹**：
  * 包含设备制造商提供的驱动和硬件相关文件。
  * 通常用于确保设备硬件与系统兼容。

* **`radio.img` 或 `modem.img`**：
  * 包含基带（Modem）固件，负责管理设备的通信功能（如蜂窝网络、Wi-Fi等）。
  * 刷机时会将此文件写入设备的`modem`分区。

---

### 2. **系统应用和库**

这些文件位于`system/`文件夹中，是Android系统的核心组成部分。

* **`system/app/`**：
  * 包含系统预装的应用（APK文件），如设置、电话、短信等。
  * 这些应用是系统的一部分，用户无法直接卸载。

* **`system/priv-app/`**：
  * 包含具有更高权限的系统应用，如系统UI、联系人存储等。
  * 这些应用通常需要访问敏感数据或系统功能。

* **`system/lib/` 和 `system/lib64/`**：
  * 包含系统库文件（`.so`文件），用于支持系统应用和功能的运行。
  * `lib/`是32位库，`lib64/`是64位库。

* **`system/framework/`**：
  * 包含Android框架的核心文件（如`framework-res.apk`），用于支持系统运行和应用程序开发。

* **`system/etc/`**：
  * 包含系统配置文件，如网络配置、音频配置、权限配置等。
  * 例如：`hosts`文件、`apns-conf.xml`（APN配置）等。

* **`system/bin/` 和 `system/xbin/`**：
  * 包含系统二进制文件（可执行文件），用于执行底层命令和操作。
  * `xbin/`通常包含额外的工具，如BusyBox。

---

### 3. **用户数据和缓存**

这些文件通常位于`data/`和`cache/`分区中，但在ROM中可能以占位符或空文件夹的形式存在。

* **`data/`**：
  * 包含用户数据和应用程序数据。
  * 刷机时通常会清除此分区。

* **`cache/`**：
  * 包含系统缓存和临时文件。
  * 刷机时通常会清除此分区。

---

### 4. **刷机脚本**

这些文件用于控制刷机过程，通常位于ROM的根目录或`META-INF/`文件夹中。

* **`META-INF/`**：
  * 包含刷机脚本和签名信息。
  * **`updater-script`**：定义刷机过程中的操作，如格式化分区、解压文件等。
  * **`MANIFEST.MF`**：包含ROM文件的校验信息。
  * **`CERT.RSA` 和 `CERT.SF`**：用于验证ROM的签名。

---

### 5. **其他文件**

这些文件可能因ROM类型（官方ROM或第三方ROM）而有所不同。

* **`bootanimation.zip`**：
  * 包含设备的启动动画。
  * 位于`system/media/`或`system/product/media/`中。

* **`fonts/`**：
  * 包含系统字体文件。
  * 位于`system/fonts/`中。

* **`media/`**：
  * 包含系统音效、铃声、通知音等。
  * 位于`system/media/audio/`中。

* **`odm/` 和 `product/`**：
  * 包含设备制造商或运营商定制的文件。
  * 这些文件通常用于添加特定功能或应用。

---

### 6. **GApps（Google Apps）**

在第三方ROM中，Google应用通常不包含在ROM中，需要单独刷入。

* **`GApps` 包**：
  * 包含Google Play商店、Gmail、Google Maps等Google应用。
  * 通常以ZIP文件形式提供，刷机时通过Recovery刷入。

---

### 7. **Magisk（可选）**

用于获取Root权限和管理模块。

* **`Magisk.zip`**：
  * 包含Magisk安装文件，刷入后可以获取Root权限。
  * 还可以通过Magisk模块扩展系统功能。

---

### 最后总结

Android系统的ROM是一个复杂的文件集合，包含系统核心文件、应用、库、配置文件和刷机脚本等。不同ROM（官方或第三方）的文件结构可能有所不同，但核心功能相似。刷机时，这些文件会被写入设备的相应分区，从而完成系统的安装或更新。理解ROM的文件结构有助于更好地进行刷机、调试和定制。
