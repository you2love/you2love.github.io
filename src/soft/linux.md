# linux
<!-- toc --> 

## 文件挂载

在Linux中，文件挂载是将存储设备（如硬盘、分区、USB驱动器等）或远程文件系统连接到文件系统树中的某个目录，使得该设备或文件系统的内容可以通过该目录访问。挂载点是文件系统树中的一个目录，挂载后，该目录的内容会被挂载设备的内容替代。

### 1. 挂载的基本概念

- **挂载点**：文件系统树中的一个目录，用于访问挂载设备的内容。
- **挂载设备**：可以是物理设备（如硬盘分区）或虚拟设备（如网络文件系统）。
- **文件系统类型**：如ext4、NTFS、FAT32等。

### 2. 挂载命令

`mount` 是Linux中用于挂载文件系统的主要命令。

#### 基本语法

```bash
mount [选项] <设备> <挂载点>
```

#### 示例

```bash
sudo mount /dev/sdb1 /mnt/mydisk
```

- `/dev/sdb1` 是要挂载的设备。
- `/mnt/mydisk` 是挂载点。

### 3. 卸载命令

`umount` 用于卸载已挂载的文件系统。

```bash
umount <挂载点或设备>
```

```bash
sudo umount /mnt/mydisk
```

或

```bash
sudo umount /dev/sdb1
```

### 4. 查看已挂载的文件系统

使用 `mount` 命令查看当前挂载的文件系统：

```bash
mount
```

或使用 `df` 命令查看磁盘使用情况：

```bash
df -h
```

### 5. 自动挂载

通过编辑 `/etc/fstab` 文件，可以在系统启动时自动挂载文件系统。

#### `/etc/fstab` 文件格式

```plaintext
<设备> <挂载点> <文件系统类型> <选项> <dump> <pass>
```

```plaintext
/dev/sdb1 /mnt/mydisk ext4 defaults 0 2
```

- `defaults` 是挂载选项。
- `0` 表示不备份。
- `2` 表示在启动时进行文件系统检查。

### 6. 挂载选项

挂载时可以指定多种选项，如：

- `ro`：只读挂载。
- `rw`：读写挂载。
- `noexec`：禁止执行文件。
- `nosuid`：禁止设置用户ID和组ID。

```bash
sudo mount -o ro /dev/sdb1 /mnt/mydisk
```

### 7. 挂载网络文件系统

Linux支持挂载远程文件系统，如NFS和CIFS。

#### 挂载NFS

```bash
sudo mount -t nfs <NFS服务器>:<导出目录> <挂载点>
```

#### 挂载CIFS（Windows共享）

```bash
sudo mount -t cifs //<服务器>/<共享目录> <挂载点> -o username=<用户>,password=<密码>
```

### 8. 挂载ISO文件

可以将ISO文件挂载为只读文件系统。

```bash
sudo mount -o loop /path/to/image.iso /mnt/iso
```

### 9. 挂载临时文件系统

可以使用 `tmpfs` 挂载临时文件系统到内存中。

```bash
sudo mount -t tmpfs tmpfs /mnt/tmp
```

### 10. 挂载LVM卷

如果使用LVM（逻辑卷管理），可以挂载逻辑卷。

```bash
sudo mount /dev/vgname/lvname /mnt/mylv
```

### 11. 挂载加密文件系统

如LUKS加密的分区，需要先解密再挂载。

```bash
sudo cryptsetup open /dev/sdb1 my_encrypted_volume
sudo mount /dev/mapper/my_encrypted_volume /mnt/encrypted
```

### 12. 挂载错误处理

- **设备忙**：确保没有进程在使用挂载点。
- **权限不足**：使用 `sudo` 提升权限。
- **文件系统损坏**：使用 `fsck` 检查和修复。

### 13. 挂载虚拟文件系统

如 `proc` 和 `sysfs`，通常由系统自动挂载。

```bash
sudo mount -t proc proc /proc
sudo mount -t sysfs sysfs /sys
```

### 总结

文件挂载是Linux系统中管理存储设备和文件系统的重要操作。通过 `mount` 和 `umount` 命令，可以手动挂载和卸载文件系统。通过 `/etc/fstab` 文件，可以实现自动挂载。挂载选项和文件系统类型的选择可以根据需求进行调整。

## 启动流程

Linux系统的启动过程是一个复杂的过程，涉及多个阶段和组件的协同工作。以下是Linux启动过程的详细步骤：

### 1. BIOS/UEFI 阶段

- **BIOS (Basic Input/Output System)** 或 **UEFI (Unified Extensible Firmware Interface)** 是计算机启动时首先运行的固件。
- **BIOS/UEFI** 进行硬件自检（POST, Power-On Self-Test），检查硬件设备是否正常工作。
- **BIOS/UEFI** 根据配置的启动顺序（Boot Order）查找可启动设备（如硬盘、USB、光盘等）。
- **BIOS/UEFI** 加载并执行启动设备的第一个扇区（MBR, Master Boot Record）或UEFI分区中的引导程序。

### 2. Boot Loader 阶段

- **Boot Loader** 是启动过程中的第二个阶段，负责加载操作系统内核。
- 常见的Boot Loader有 **GRUB (GRand Unified Bootloader)** 和 **LILO (LInux LOader)**。
- **GRUB** 是大多数现代Linux发行版使用的Boot Loader。

#### GRUB 的工作流程

1. **GRUB** 加载其配置文件（通常位于 `/boot/grub/grub.cfg`）。
2. 显示启动菜单，允许用户选择要启动的操作系统或内核版本。
3. 加载选定的Linux内核映像（`vmlinuz`）和初始内存盘（`initrd` 或 `initramfs`）。

### 3. 内核初始化阶段

- **内核** 是操作系统的核心，负责管理硬件资源和系统进程。
- 内核被加载到内存后，开始初始化：
  1. 解压缩内核映像。
  2. 设置硬件设备驱动程序。
  3. 挂载根文件系统（`/`）。
  4. 启动第一个用户空间进程（`init` 或 `systemd`）。

### 4. initramfs 阶段

- **initramfs** 是一个临时的根文件系统，包含启动过程中所需的工具和驱动程序。
- **initramfs** 的主要任务是加载必要的硬件驱动程序和挂载真正的根文件系统。
- 一旦真正的根文件系统被挂载，**initramfs** 会被卸载，控制权交给真正的根文件系统。

### 5. 用户空间初始化阶段

- 在根文件系统挂载后，内核启动第一个用户空间进程（通常是 `init` 或 `systemd`）。
- **init** 或 **systemd** 是用户空间的第一个进程（PID 1），负责启动和管理其他系统服务和进程。

#### init 系统的工作流程

1. **init** 读取其配置文件（通常是 `/etc/inittab`）。
2. 根据运行级别（Runlevel）启动相应的服务和进程。
3. 运行级别定义了系统启动时运行的服务和进程。

#### systemd 系统的工作流程

1. **systemd** 读取其配置文件（通常是 `/etc/systemd/system/default.target`）。
2. 根据目标（Target）启动相应的服务和进程。
3. **systemd** 提供了更强大的服务管理和并行启动能力。

### 6. 运行级别（Runlevel）或目标（Target）

- **运行级别** 是传统 `init` 系统的概念，定义了系统启动时运行的服务和进程。
- **目标** 是 `systemd` 系统的概念，类似于运行级别，但更灵活和强大。

#### 常见的运行级别

- **0**：关机
- **1**：单用户模式（维护模式）
- **2**：多用户模式（无网络）
- **3**：多用户模式（有网络）
- **4**：保留
- **5**：图形界面模式
- **6**：重启

#### 常见的 systemd 目标

- **poweroff.target**：关机
- **rescue.target**：救援模式
- **multi-user.target**：多用户模式
- **graphical.target**：图形界面模式
- **reboot.target**：重启

### 7. 启动服务和进程

- **init** 或 **systemd** 根据运行级别或目标启动相应的服务和进程。
- 这些服务包括网络服务、日志服务、用户登录服务等。
- 一旦所有必要的服务和进程启动完成，系统进入可用的状态，用户可以登录并使用系统。

### 8. 用户登录

- 系统启动完成后，显示登录界面（图形界面或命令行界面）。
- 用户输入用户名和密码进行登录。
- 登录成功后，用户进入系统并可以使用各种应用程序和服务。

### 最后

Linux系统的启动过程可以分为以下几个主要阶段：

1. **BIOS/UEFI** 阶段：硬件自检和加载Boot Loader。
2. **Boot Loader** 阶段：加载内核和initramfs。
3. **内核初始化** 阶段：初始化硬件和挂载根文件系统。
4. **initramfs** 阶段：加载必要的驱动程序和挂载真正的根文件系统。
5. **用户空间初始化** 阶段：启动第一个用户空间进程（init或systemd）。
6. **运行级别或目标**：根据配置启动相应的服务和进程。
7. **启动服务和进程**：启动系统服务和用户进程。
8. **用户登录**：用户登录并使用系统。

每个阶段都有其特定的任务和组件，共同协作完成系统的启动过程。
