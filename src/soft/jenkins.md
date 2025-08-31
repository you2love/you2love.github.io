
<!-- toc --> 
# jenkins

## 动作

* 重启-直接在地址后面加个 /restart

```bash
https://jenkins.xxx/restart
```

* 退出-直接在地址后面加个/exit

```bash
https://jenkins.xxx/exit
```

* 出现错误

```bash
# 一般是私钥的-----BEGIN OPENSSH PRIVATE KEY-----没有复制全
stderr: Load key "/tmp/jenkins-gitclient-ssh7026290831916999837.key": invalid format 
```

* 复制到远程主机

  * 安装publish-over-ssh插件

Jenkins 是一个开源的持续集成和持续交付（CI/CD）工具，广泛用于自动化软件构建、测试和部署。以下是 Jenkins 的核心概念及其详细解释，帮助你理解它的工作原理和核心功能：

---

### 1. **Pipeline（流水线）**

* **定义**：Pipeline 是 Jenkins 的核心概念，用于定义自动化流程（如构建、测试、部署），通过代码（Jenkinsfile）描述整个过程。
* **特点**：
  * 使用 **Declarative Pipeline**（声明式语法）或 **Scripted Pipeline**（脚本式语法）编写。
  * 支持多阶段（`stages`）、并行任务、错误处理等复杂逻辑。
* **示例**：

     ```groovy
     pipeline {
         agent any
         stages {
             stage('Build') {
                 steps {
                     sh 'mvn clean package'
                 }
             }
             stage('Test') {
                 steps {
                     sh 'mvn test'
                 }
             }
         }
     }
     ```

---

### 2. **节点（Node）与代理（Agent）**

* **节点（Node）**：指 Jenkins 环境中的物理或虚拟机器（如服务器、Docker 容器）。
* **代理（Agent）**：在节点上运行的程序，负责执行具体的任务（如构建）。
* **主节点（Master）**：Jenkins 控制中心，管理任务调度、界面展示等，不推荐直接执行任务。
* **工作节点（Slave/Agent）**：实际执行任务的节点，支持分布式构建。

---

### 3. **Job/Project（任务/项目）**

* **定义**：Job 是 Jenkins 中一个可配置的自动化任务单元，代表一个具体的构建流程。
* **类型**：
  * **Freestyle Project**：通过界面配置的简单任务。
  * **Pipeline Job**：基于 Jenkinsfile 的复杂流水线任务。
  * **Multi-configuration Project**：支持多环境（如不同操作系统、浏览器）并行测试。

---

### 4. **Build（构建）**

* **定义**：Job 的一次具体执行，生成日志、测试报告、构建产物（Artifacts）等。
* **构建历史**：保留每次构建的结果（成功/失败）、日志和产出，便于调试和分析。

---

### 5. **Executor（执行器）**

* **定义**：节点上的执行线程，决定同时运行的构建数量。例如，一个节点有 2 个 Executor 可并行执行 2 个任务。

---

### 6. **插件（Plugin）**

* **作用**：扩展 Jenkins 功能（如集成 Git、Docker、Kubernetes、消息通知等）。
* **常见插件**：
  * **Git Plugin**：从 Git 仓库拉取代码。
  * **Docker Pipeline**：集成 Docker 容器。
  * **Email Extension**：发送构建通知邮件。

---

### 7. **Workspace（工作区）**

* **定义**：节点上为 Job 分配的专属目录，存放源代码、构建产物和临时文件。
* **清理**：每次构建前可配置清理工作区，避免旧文件干扰。

---

### 8. **Trigger（触发器）**

* **定义**：触发构建的条件，常见类型：
  * **SCM 变更**（如 Git 提交）。
  * **定时触发**（如 `H/15 * * * *` 每 15 分钟）。
  * **手动触发**（用户点击构建按钮）。
  * **上游任务触发**（其他 Job 完成后触发）。

---

### 9. **Credential（凭证）**

* **作用**：安全存储敏感信息（如 Git 密码、SSH 密钥、API Token）。
* **类型**：支持用户名密码、密钥文件、Secret Text 等。

---

### 10. **Distributed Build（分布式构建）**

* **场景**：将任务分发到多个节点执行，加速构建或适配不同环境（如跨平台测试）。
* **配置**：通过 Jenkins 管理界面添加工作节点并分配标签（Label）。

---

### 11. **Shared Library（共享库）**

* **定义**：将通用的 Pipeline 代码封装为库，供多个项目复用。
* **存储**：通常托管在 Git 仓库中，通过 Jenkins 全局配置引入。

---

### 12. **Blue Ocean**

* **定义**：Jenkins 的现代化 UI，提供可视化流水线编辑和构建状态展示。
* **功能**：直观的 Pipeline 设计器、实时日志、分支和拉取请求集成。

---

### 13. **安全性**

* **认证（Authentication）**：用户登录验证（如 LDAP、GitHub OAuth）。
* **授权（Authorization）**：权限控制（如基于角色的权限管理插件 Role-Based Strategy）。

---

### 14. **其他关键概念**

* **File Fingerprinting（文件指纹）**：跟踪文件版本，用于依赖管理。
* **Artifact（构建产物）**：构建生成的二进制文件、报告等，可存档或分发。
* **Environment Variables（环境变量）**：全局或 Job 级别的变量（如 `BUILD_NUMBER`）。
* **Parameterized Build（参数化构建）**：允许用户输入参数（如版本号、环境类型）后再执行构建。

---

### 应用场景示例

1. **自动化测试**：每次代码提交后自动运行单元测试和集成测试。
2. **持续交付**：构建成功后自动部署到测试环境，手动审批后发布到生产环境。
3. **多环境部署**：通过分布式构建在不同节点上部署到不同云平台（如 AWS、Azure）。

---

### 总结

Jenkins 的核心在于通过 **Pipeline 即代码** 和 **插件扩展** 实现高度灵活和可定制的自动化流程。掌握这些概念后，可以结合具体需求设计高效的 CI/CD 流水线，提升软件交付速度和质量。如需深入学习，建议从官方文档和实际项目实践入手。
