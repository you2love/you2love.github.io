# Android

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

在 Android 设备中，各个分区会被挂载到特定的目录下，这些目录是文件系统的一部分，用于访问和管理分区中的数据。以下是常见的 Android 分区及其挂载点的详细说明：

---

在 Android 设备中，**fstab（文件系统表）** 是一个配置文件，用于定义设备分区的挂载信息。它告诉系统在启动时如何挂载各个分区（如 `system`、`data`、`cache` 等）。以下是关于 `fstab` 的详细说明以及如何查看它的方法。

---

## fstab介绍

### 1. **fstab 的作用**

* **定义分区挂载点**：指定每个分区的挂载路径（如 `/system`、`/data` 等）。
* **设置文件系统类型**：指定分区的文件系统类型（如 `ext4`、`f2fs` 等）。
* **配置挂载选项**：设置挂载时的参数（如 `ro` 只读、`rw` 读写等）。
* **控制分区权限**：定义分区的访问权限和所有者。

---

### 2. **fstab 文件的位置**

`fstab` 文件通常位于以下位置之一：

1. **`/etc/fstab`**：
   * 在某些设备上，`fstab` 文件可能直接位于 `/etc/` 目录下。
2. **`/system/etc/recovery.fstab`**：
   * 这是 Recovery 模式使用的 `fstab` 文件，定义了 Recovery 模式下如何挂载分区。
3. **`/vendor/etc/fstab.<device>`**：
   * 在某些设备上，`fstab` 文件可能位于 `/vendor/etc/` 目录下，并以设备名称命名（如 `fstab.qcom`）。
4. **`/odm/etc/fstab.<device>`**：
   * 在某些设备上，`fstab` 文件可能位于 `/odm/etc/` 目录下。

---

### 3. **如何查看 fstab 文件**

#### **方法 1：通过 ADB 查看**

1. **连接设备**：
   * 使用 USB 线将设备连接到电脑，并启用 USB 调试模式。
2. **打开终端或命令提示符**：
   * 输入以下命令查看 `fstab` 文件：

     ```bash
     adb shell cat /system/etc/recovery.fstab
     ```

   * 如果文件不在默认位置，可以尝试以下命令：

     ```bash
     adb shell find / -name "fstab*"
     ```

   * 找到文件后，使用 `cat` 命令查看内容。

#### **方法 2：通过终端模拟器查看**

1. **安装终端模拟器**：
   * 在设备上安装终端模拟器应用（如 Termux 或 Android Terminal Emulator）。
2. **运行命令**：
   * 输入以下命令查看 `fstab` 文件：

     ```bash
     cat /system/etc/recovery.fstab
     ```

   * 如果文件不在默认位置，可以使用 `find` 命令查找：

     ```bash
     find / -name "fstab*"
     ```

#### **方法 3：通过 Recovery 查看**

1. **进入 Recovery 模式**：
   * 关机后按住特定组合键（如音量上 + 电源键）进入 Recovery 模式。
2. **挂载系统分区**：
   * 在 Recovery 中选择挂载 `system` 分区。
3. **查看文件**：
   * 使用 Recovery 的文件管理器或终端功能查看 `/system/etc/recovery.fstab`。

---

### 4. **fstab 文件的内容示例**

以下是一个典型的 `fstab` 文件内容示例：

```plaintext
#<src>          <mnt_point>     <type>  <mnt_flags>                             <fs_mgr_flags>
/dev/block/bootdevice/by-name/system       /system         ext4    ro,barrier=1                                  wait,avb
/dev/block/bootdevice/by-name/userdata     /data           ext4    noatime,nosuid,nodev,barrier=1,data=ordered    wait,forceencrypt=footer
/dev/block/bootdevice/by-name/cache        /cache          ext4    noatime,nosuid,nodev,barrier=1,data=ordered    wait
/dev/block/bootdevice/by-name/persist      /persist        ext4    nosuid,nodev,barrier=1                         wait
/dev/block/bootdevice/by-name/modem        /firmware       vfat    ro,shortname=lower,uid=1000,gid=1000,dmask=227,fmask=337  wait
```

* **`<src>`**：分区的块设备路径（如 `/dev/block/bootdevice/by-name/system`）。

* **`<mnt_point>`**：分区的挂载点（如 `/system`）。
* **`<type>`**：文件系统类型（如 `ext4`、`vfat` 等）。
* **`<mnt_flags>`**：挂载选项（如 `ro` 只读、`noatime` 不更新访问时间等）。
* **`<fs_mgr_flags>`**：文件系统管理器选项（如 `wait` 等待分区就绪、`forceencrypt` 强制加密等）。

---

### 5. **注意事项**

* **不要随意修改 `fstab` 文件**：错误的修改可能导致设备无法启动或分区无法挂载。

* **备份原始文件**：在修改 `fstab` 文件之前，务必备份原始文件。
* **设备差异**：不同设备的 `fstab` 文件位置和内容可能有所不同。

---

### 6. **总结**

`fstab` 文件是 Android 设备中用于定义分区挂载信息的重要配置文件。它通常位于 `/system/etc/recovery.fstab` 或 `/vendor/etc/fstab.<device>` 等路径下。通过 ADB、终端模拟器或 Recovery 模式，可以查看和编辑 `fstab` 文件。理解 `fstab` 文件的作用和内容，有助于更好地管理和调试 Android 设备。

## 分区挂载

### 1. **常见的 Android 分区及其挂载点**

| 分区名称         | 挂载点（目录）       | 作用描述                                                                 |
|------------------|----------------------|------------------------------------------------------------------------|
| **`system`**     | `/system`            | 包含 Android 操作系统、系统应用和库文件。                               |
| **`vendor`**     | `/vendor`            | 包含设备制造商提供的驱动和硬件相关文件。                                |
| **`data`**       | `/data`              | 包含用户数据、应用程序数据和个人文件。                                  |
| **`cache`**      | `/cache`             | 用于存储临时文件和系统缓存。                                            |
| **`persist`**    | `/persist`           | 存储持久化数据，如设备的校准信息和传感器数据。                          |
| **`misc`**       | `/misc`              | 存储一些杂项信息，如 Bootloader 的启动标志。                            |
| **`firmware`**   | `/firmware`          | 包含设备的固件文件（如基带固件）。                                      |
| **`odm`**        | `/odm`               | 包含设备制造商的自定义文件（如品牌 Logo、预装应用等）。                 |
| **`metadata`**   | `/metadata`          | 用于加密文件系统的元数据分区。                                          |
| **`sdcard`**     | `/storage/emulated/0`| 外部存储分区，用于存储用户文件（如照片、视频等）。                      |
| **`userdata`**   | `/data`              | 与 `data` 分区类似，某些设备将 `data` 和 `userdata` 合并。              |
| **`boot`**       | 无挂载点             | 包含内核和初始内存磁盘，用于启动设备，不挂载到文件系统。                |
| **`recovery`**   | 无挂载点             | 包含 Recovery 模式，用于系统恢复和更新，不挂载到文件系统。              |

---

### 2. **挂载点的作用**

* **`/system`**：
  * 包含 Android 系统的核心文件，如系统应用、库文件和配置文件。
  * 通常以只读（`ro`）方式挂载，防止用户误修改系统文件。

* **`/vendor`**：
  * 包含设备制造商提供的驱动和硬件相关文件。
  * 用于确保设备硬件与系统兼容。
* **`/data`**：
  * 包含用户数据和应用程序数据。
  * 是用户存储文件、安装应用和保存设置的主要位置。
* **`/cache`**：
  * 用于存储临时文件和系统缓存。
  * 可以安全清除，用于解决系统卡顿或更新问题。
* **`/persist`**：
  * 存储持久化数据，如设备的校准信息和传感器数据。
  * 即使恢复出厂设置，数据也不会被清除。
* **`/firmware`**：
  * 包含设备的固件文件，如基带（Modem）固件。
  * 用于管理设备的通信功能（如蜂窝网络、Wi-Fi 等）。
* **`/odm`**：
  * 包含设备制造商的自定义文件，如品牌 Logo 和预装应用。
  * 用于提供设备的定制化功能。
* **`/metadata`**：
  * 用于加密文件系统的元数据分区。
  * 在启用文件系统加密时使用。
* **`/storage/emulated/0`**：
  * 外部存储分区，用于存储用户文件（如照片、视频等）。
  * 在 Android 中，外部存储通常被模拟为 `/storage/emulated/0`。

---

### 3. **如何查看分区的挂载信息**

可以通过以下方法查看 Android 设备的分区挂载信息：

#### **方法 1：通过 ADB 命令查看**

1. **连接设备**：
   * 使用 USB 线将设备连接到电脑，并启用 USB 调试模式。
2. **打开终端或命令提示符**：
   * 输入以下命令查看挂载信息：

     ```bash
     adb shell mount
     ```

   * 或者查看 `/proc/mounts` 文件：

     ```bash
     adb shell cat /proc/mounts
     ```

#### **方法 2：通过终端模拟器查看**

1. **安装终端模拟器**：
   * 在设备上安装终端模拟器应用（如 Termux 或 Android Terminal Emulator）。
2. **运行命令**：
   * 输入以下命令查看挂载信息：

     ```bash
     mount
     ```

   * 或者查看 `/proc/mounts` 文件：

     ```bash
     cat /proc/mounts
     ```

#### **方法 3：通过文件管理器查看**

1. **安装文件管理器**：
   * 在设备上安装支持 Root 权限的文件管理器（如 Solid Explorer、Root Explorer）。
2. **查看挂载点**：
   * 导航到根目录（`/`），查看各个挂载点（如 `/system`、`/data` 等）。

---

### 4. **挂载点的示例输出**

以下是 `adb shell mount` 或 `mount` 命令的示例输出：

```plaintext
/dev/block/bootdevice/by-name/system on /system type ext4 (ro,seclabel,relatime)
/dev/block/bootdevice/by-name/vendor on /vendor type ext4 (ro,seclabel,relatime)
/dev/block/bootdevice/by-name/userdata on /data type ext4 (rw,seclabel,nosuid,nodev,noatime)
/dev/block/bootdevice/by-name/cache on /cache type ext4 (rw,seclabel,nosuid,nodev,noatime)
/dev/block/bootdevice/by-name/persist on /persist type ext4 (rw,seclabel,nosuid,nodev,noatime)
```

* **`/dev/block/bootdevice/by-name/system`**：分区的块设备路径。

* **`/system`**：挂载点。
* **`ext4`**：文件系统类型。
* **`(ro,seclabel,relatime)`**：挂载选项。

---

### 5. **总结**

Android 设备的分区会挂载到特定的目录下，如 `/system`、`/data`、`/cache` 等。这些挂载点是文件系统的一部分，用于访问和管理分区中的数据。通过 ADB、终端模拟器或文件管理器，可以查看分区的挂载信息。理解分区挂载点的作用，有助于更好地管理和调试 Android 设备。

## /sdcard/Android/data

`/sdcard/Android/data` 是 Android 系统中一个非常重要的目录，主要用于存储应用程序的**私有数据**和**缓存文件**。以下是它的具体作用和特点

---

### 1. **目录用途**

* **应用程序私有数据**：
  * 每个应用程序在 `/sdcard/Android/data/<package_name>/` 目录下都有一个专属的子目录。
  * 应用程序可以将自己的数据（如缓存、配置文件、临时文件等）存储在这里。
  * 这些数据是应用程序私有的，其他应用程序无法直接访问（除非有特殊权限）。

* **缓存文件**：
  * 应用程序可以将临时文件或缓存数据存储在这里，以加快加载速度或减少网络请求。
  * 系统在存储空间不足时，可能会自动清理这些缓存文件。

---

### 2. **目录结构**

* 路径示例：

  ```shell
  /sdcard/Android/data/com.example.app/
  ```

  * `com.example.app` 是应用程序的包名。
  * 每个应用程序的目录是独立的，互不干扰。

* 子目录示例：
  * `cache/`：用于存储缓存文件。
  * `files/`：用于存储应用程序的私有文件。
  * 其他自定义目录：应用程序可以根据需要创建自己的子目录。

---

### 3. **访问权限**

* **应用程序权限**：
  * 应用程序无需额外权限即可访问自己的 `/sdcard/Android/data/<package_name>/` 目录。
  * 其他应用程序无法直接访问该目录（除非使用 `MANAGE_EXTERNAL_STORAGE` 权限，但需要用户授权）。

* **用户访问**：
  * 用户可以通过文件管理器访问 `/sdcard/Android/data/` 目录。
  * 从 Android 11（API 级别 30）开始，应用程序对 `/sdcard/Android/data/` 的访问受到更严格的限制，普通文件管理器可能无法直接访问其他应用程序的目录。

---

### 4. **与 `/data/data/` 的区别**

* `/data/data/<package_name>/`：
  * 位于内部存储中，是应用程序的**真正私有目录**。
  * 只有应用程序本身和系统可以访问，用户和第三方应用程序无法直接访问。
  * 存储应用程序的核心数据、数据库、SharedPreferences 等。

* `/sdcard/Android/data/<package_name>/`：
  * 位于外部存储（如内部存储的模拟 SD 卡分区或物理 SD 卡）中。
  * 存储应用程序的非核心数据（如缓存、下载的文件等）。
  * 用户和文件管理器可以访问，但受权限限制。

---

### 5. **清理机制**

* **系统自动清理**：
  * 当设备存储空间不足时，系统会自动清理 `/sdcard/Android/data/` 目录下的缓存文件。
  * 应用程序可以通过 `Context.getExternalCacheDir()` 获取缓存目录。

* **用户手动清理**：
  * 用户可以通过设备的“设置” > “存储” > “清理缓存”来删除缓存文件。
  * 用户也可以通过文件管理器手动删除 `/sdcard/Android/data/` 目录下的文件。

---

### 6. **开发者注意事项**

* **存储位置**：
  * 使用 `Context.getExternalFilesDir()` 和 `Context.getExternalCacheDir()` 获取应用程序的私有目录。
  * 示例：

    ```java
    File externalFilesDir = getExternalFilesDir(null); // 返回 /sdcard/Android/data/<package_name>/files/
    File externalCacheDir = getExternalCacheDir();     // 返回 /sdcard/Android/data/<package_name>/cache/
    ```

* **兼容性**：
  * 从 Android 11 开始，访问 `/sdcard/Android/data/` 目录需要 `MANAGE_EXTERNAL_STORAGE` 权限。
  * 开发者应遵循 Android 的存储访问框架（SAF）来访问共享存储。

---

### 总结一下

`/sdcard/Android/data/` 是 Android 系统中用于存储应用程序私有数据和缓存文件的目录。它具有以下特点：

* 每个应用程序有独立的子目录。
* 数据是私有的，其他应用程序无法直接访问。
* 用户和系统可以清理缓存文件。
* 开发者应使用系统提供的 API 来访问该目录，以确保兼容性和安全性。

## 适用于PC的最佳安卓操作系统

* [Bliss OS](https://blissos.org/)：这是一个出色的安卓操作系统，专为在PC上实现安卓文化而努力。自推出以来，它一直表现良好，被专家标记为最好的安卓操作系统之一
* Remix OS：由JIDE公司创建，专为PC用户提供梦幻般的体验。虽然只支持基于英特尔的计算机，但它仍然是一个受欢迎的选择
* OPENTH OS：另一个适用于PC的操作系统，提供完整的功能，但只能在64位计算机上运行。它具有出色的导航和用户界面
* Android X86：这个操作系统基于安卓源代码，设计为在具有AMD和Intel x86处理器的设备上运行。它与安卓的原始版本非常相似，易于下载和安装
* 凤凰系统 Phoenix OS：由中国公司开发，与Remix OS竞争。它提供了一些很酷和不寻常的应用程序，用户界面也非常简单
* Chrome OS：适用于Chromebook的顶级安卓系统，专为非技术人员设计，提供高性能
* [PrimeOS](https://www.primebook.in)：适用于笔记本电脑和个人电脑的出色安卓操作系统，具有令人难以置信的外观和DecaPro工具
* 沿袭系统 Lineage OS：基于Marshmallow安卓版本6，具有快速安装和更好的界面
