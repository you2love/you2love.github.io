一、核心载体：容器与Pod
这是k8s里最小的部署和运行单元，是所有概念的基础。

Pod
- 定义：k8s中最小的可部署单元，不是容器，而是一组紧密关联的容器的集合（通常1个Pod里跑1个主容器+若干辅助容器）。
- 特点：同一个Pod内的容器共享网络命名空间（可以用localhost互相通信）和存储卷；Pod是临时性的，被删除或故障后不会恢复，而是由控制器重新创建。
- 实例YAML（精简）：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels: {app: nginx}
spec:
  containers:
  - name: nginx-container
    image: nginx:1.25
    ports: [{containerPort: 80}]
```

容器（Container）
- 定义：就是Docker这类容器技术打包的应用，Pod是容器的“外壳”，k8s通过管理Pod来间接管理容器。

二、调度与管理：控制器（Controller）
控制器是k8s的“调度大脑”，负责确保Pod的实际状态和你声明的期望状态一致（比如你要3个Pod副本，它就会维持3个，少了就补）。

1. Deployment
- 用途：最常用的控制器，用于管理无状态应用（比如前端、后端API）。
- 核心功能：支持滚动更新（逐个替换旧Pod，不中断服务）、回滚（更新出问题时一键退回旧版本）、扩缩容。
- 常用操作：
  - 扩缩容：`kubectl scale deployment nginx-deploy --replicas=5`
  - 滚动更新：`kubectl set image deployment nginx-deploy nginx=nginx:1.26`

2. StatefulSet
- 用途：用于管理有状态应用（比如数据库、Redis集群）。
- 核心特点：Pod有固定的名称和网络标识，存储卷和Pod绑定，重启后身份不变，适合需要持久化状态的应用。

3. DaemonSet
- 用途：确保集群中每一个节点（或指定节点）都运行一个Pod副本。
- 典型场景：日志收集（比如Fluentd）、监控代理（比如Prometheus Node Exporter）。

4. Job/CronJob
- Job：用于运行一次性任务（比如数据备份、批量计算），任务完成后Pod自动结束。
- CronJob：基于时间的定时任务（类似Linux的crontab），比如每天凌晨备份数据库。

5. ReplicaSet（RS）
- 用途：直接管理Pod的副本数量，确保集群中始终有指定数量的Pod在运行。Deployment就是基于ReplicaSet实现的，日常使用中一般直接用Deployment即可。

三、服务访问：Service & Ingress
Pod的IP是动态的（重启后会变），这两类概念解决“如何稳定访问Pod”的问题。

1. Service
- 定义：为一组相同功能的Pod提供固定的访问入口和负载均衡。
- 核心类型：
  - ClusterIP：默认类型，仅在集群内部可访问，用于集群内服务间通信（比如前端Pod访问后端Pod）。
  - NodePort：在集群每个节点上开放一个固定端口，外部可以通过节点IP:端口访问服务，适合测试环境。
  - LoadBalancer：结合云厂商的负载均衡器，自动分配公网IP，适合生产环境暴露服务。

2. Ingress
- 定义：相当于k8s的“智能反向代理”，解决Service无法满足的复杂HTTP/HTTPS路由需求。
- 核心功能：域名路由（比如api.example.com指向后端服务，web.example.com指向前端服务）、SSL证书管理、路径匹配（比如/api转发到API服务）。
- 注意：Ingress本身只是规则，需要部署Ingress Controller（比如Nginx Ingress Controller）才能生效。

四、配置与存储：ConfigMap、Secret、Volume、PV/PVC
解决“应用配置管理”和“数据持久化”的问题。

1. ConfigMap
- 用途：用于存储非敏感的配置数据（比如配置文件、环境变量、命令行参数）。
- 特点：可以和Pod解耦，修改ConfigMap后可以热更新Pod的配置，不用重建镜像。

2. Secret
- 用途：用于存储敏感信息（比如密码、Token、SSL证书）。
- 特点：数据会被Base64编码存储（注意：不是加密，生产环境建议结合密钥管理工具），可以挂载到Pod里作为文件或环境变量。

3. Volume
- 用途：用于Pod内的容器共享存储，或临时存储数据。
- 常见类型：
  - emptyDir：Pod生命周期内的临时存储，Pod删除后数据丢失。
  - hostPath：挂载节点的本地目录，适合单节点测试，不推荐生产用。

4. PersistentVolume（PV）& PersistentVolumeClaim（PVC）
- 这是一套“存储资源池”机制，解决Pod数据持久化的问题（比如数据库数据需要永久保存）。
- PV：集群管理员创建的持久化存储资源（比如云硬盘、NFS共享存储），和节点无关。
- PVC：用户（开发者）申请存储的“请求单”，声明需要的存储大小、访问模式，k8s会自动绑定匹配的PV。
- 核心优势：用户不用关心底层存储的具体实现，只需要申请PVC即可。

五、基础架构核心组件

控制平面（Control Plane）
- API Server：所有操作统一入口，接收kubectl命令调用。
- etcd：分布式键值存储，保存集群所有状态（如Pod IP、Service配置）。
- Scheduler：按资源情况、亲和性规则，将Pod调度到合适Node。
- Controller Manager：包含多种控制器，自动修复故障Pod、维持集群状态。

工作节点（Node）
- Kubelet：与API Server通信，确保Pod按规格运行，上报Node状态。
- Kube-proxy：实现Service网络规则，将请求转发到后端Pod。
- Container Runtime：容器运行时（如Docker、Containerd），负责启动/停止容器。

六、补充核心概念：Namespace & Label/Selector

1. Namespace
- 用途：集群的逻辑隔离单元，可以把不同的应用、环境（开发/测试/生产）隔离开，比如default（默认命名空间）、kube-system（k8s系统组件所在的命名空间）。
- 常用操作：
  - 创建：`kubectl create namespace prod`
  - 指定命名空间部署：`kubectl apply -f xxx.yaml -n prod`

2. Label & Selector
- 用途：k8s的“分组和筛选”机制，是实现“松耦合管理”的核心。
- Label：给资源（Pod、Service等）打标签，比如`app=web`、`env=prod`。
- Selector：通过标签筛选资源，比如Service通过Selector找到对应的Pod，控制器通过Selector管理Pod。

七、核心总结

1. 核心载体：Pod是最小部署单元，容器是应用载体，Pod为容器提供共享资源环境。
2. 调度管理：控制器确保Pod状态符合期望，不同控制器适配不同应用场景（无状态/有状态/定时任务等）。
3. 服务访问：Service提供稳定入口，Ingress解决复杂HTTP/HTTPS路由需求，保障Pod动态变化下的稳定访问。
4. 配置存储：ConfigMap/Secret管理配置，Volume/PV/PVC实现数据持久化，解耦应用与配置、存储。
5. 架构支撑：控制平面决策调度，Node节点执行运行，Namespace隔离资源，Label/Selector实现松耦合管理。