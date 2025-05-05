# k8s

Kubernetes 中的 **StatefulSet** 是专为管理有状态应用而设计的控制器，适用于需要稳定标识、持久化存储和有序部署的场景。以下是其核心要点：

---

### **1. 与 Deployment 的主要区别**

- **无状态 vs 有状态**  
  Deployment 适用于无状态应用（如 Web 前端），Pod 随机命名且替换后存储丢失；StatefulSet 为每个 Pod 提供唯一且稳定的标识（如 `web-0`, `web-1`），并绑定专属持久存储。
- **网络标识**  
  StatefulSet 的 Pod 拥有固定 DNS 名称（通过 Headless Service），支持直接通过 Pod 名称访问（如 `web-0.nginx.default.svc.cluster.local`）。

---

### **2. 核心特性**

- **稳定的网络标识**  
  每个 Pod 名称唯一且按序分配（`<statefulset-name>-<ordinal-index>`），重启或重新调度后保持不变。
- **持久化存储**  
  通过 `volumeClaimTemplates` 为每个 Pod 动态创建独立的 PVC，确保数据持久化（即使 Pod 被删除，存储仍保留）。
- **有序部署与扩缩容**  
  - **顺序创建**：按索引升序（如先 `web-0`，再 `web-1`）。
  - **逆序终止**：缩容时从最高索引开始删除。
  - 适用于主从架构（如 MySQL 主节点需优先启动）。
- **滚动更新策略**  
  支持 `RollingUpdate`（按序更新，从最高索引降序）和 `OnDelete`（需手动删除 Pod 触发更新）。

---

### **3. 典型使用场景**

- **分布式有状态应用**  
  如 ZooKeeper、etcd、Kafka 等需要固定网络标识和持久存储的服务。
- **数据库集群**  
  如 MySQL 主从复制、MongoDB 副本集，依赖稳定的节点标识和数据持久性。
- **需有序扩展的应用**  
  如需按顺序初始化节点的场景（如主节点先于从节点启动）。

---

### **4. 依赖与配置**

- **Headless Service**  
  必须关联一个 Headless Service（`clusterIP: None`），用于为 Pod 提供 DNS 解析，实现直接访问。
- **持久化存储**  
  需配置 `volumeClaimTemplates`，依赖 StorageClass 动态创建 PV，或手动预配 PV。
- **探针配置**  
  建议设置 `readinessProbe` 和 `livenessProbe`，确保应用就绪后再进行后续操作。

---

### **5. 注意事项**

- **存储保留策略**  
  Pod 删除后关联的 PVC 默认保留，需手动清理或配置删除策略（如 `persistentVolumeClaimRetentionPolicy`）。
- **应用层协调**  
  StatefulSet 仅保证 Pod 顺序，不处理应用层状态（如主从选举），需结合初始化容器或应用逻辑。
- **网络通信**  
  Pod 间通信应使用 DNS 名称而非 IP，避免因 IP 变化导致故障。

---

### **示例 YAML 片段**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"  # 关联的 Headless Service
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:  # 每个 Pod 动态创建 PVC
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast"
      resources:
        requests:
          storage: 1Gi
```

---

通过 StatefulSet，Kubernetes 能够有效管理有状态应用，提供稳定的网络、存储和部署顺序，是运行分布式数据库和集群化服务的理想选择。

在 Kubernetes 中，**Job** 和 **CronJob** 是两种用于管理**短期任务**的工作负载资源，但它们的用途和设计目标有显著区别。以下是两者的核心差异和适用场景：

---

### **1. 核心区别**

| **特性**               | **Job**                            | **CronJob**                          |
|-------------------------|------------------------------------|--------------------------------------|
| **设计目的**            | 运行**一次性任务**（如数据处理、批处理作业） | 运行**周期性任务**（如定时备份、定期清理） |
| **触发方式**            | 手动触发或由其他系统触发            | 按预定义的时间表（Cron 表达式）自动触发 |
| **任务执行模式**        | 任务运行到**成功完成**或达到重试次数 | 定期生成新的 Job 实例执行任务         |
| **生命周期**            | 任务完成后自动终止                  | 持续运行，按计划不断创建新的 Job       |
| **典型场景**            | 数据库迁移、批量计算、测试任务       | 每日日志归档、每小时数据同步、每周报告生成 |

---

### **2. 关键功能对比**

#### **(1) Job：一次性任务**

- **任务完成机制**  
  - 确保 Pod 成功运行到**完成状态**（exit code 0）。
  - 可配置 `completions`（需成功完成的 Pod 数量）和 `parallelism`（并行运行的 Pod 数）。
- **错误处理**  
  - 若 Pod 失败（exit code 非 0），Job 会根据 `backoffLimit` 自动重启 Pod。
- **资源清理**  
  - 任务完成后，Job 对象保留历史记录（默认不删除），需手动清理或通过 TTL 机制自动清理。

**示例场景**：  
运行一个数据处理任务，处理完成后自动终止。

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processor
spec:
  completions: 1    # 需要成功完成的次数
  parallelism: 1    # 并行运行的 Pod 数
  template:
    spec:
      containers:
      - name: processor
        image: data-processor:v1
      restartPolicy: Never  # Job 的 Pod 不允许 Always 重启
```

---

#### **(2) CronJob：定时任务**

- **时间调度**  
  - 使用 **Cron 表达式**（如 `0 * * * *` 表示每小时执行）定义任务计划。
  - 支持标准 Cron 语法（`分钟 小时 日 月 周几`）。
- **任务生成**  
  - 每次触发时创建一个新的 **Job 对象**来执行任务。
- **并发控制**  
  - 通过 `concurrencyPolicy` 控制并发行为：  
    - `Allow`（默认）：允许并发执行。  
    - `Forbid`：禁止并发，若前一个任务未完成则跳过新任务。  
    - `Replace`：取消未完成的任务，替换为新任务。
- **历史记录保留**  
  - 通过 `successfulJobsHistoryLimit` 和 `failedJobsHistoryLimit` 控制保留的已完成 Job 数量。

**示例场景**：  
每天凌晨 2 点执行数据库备份。

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"     # Cron 表达式（每天 2:00 AM）
  concurrencyPolicy: Forbid # 禁止并发执行
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup-tool
            image: backup-agent:v1
          restartPolicy: OnFailure  # 失败时重启容器（非 Pod）
```

---

### **3. 使用场景对比**

| **场景**                | **Job**                          | **CronJob**                        |
|-------------------------|----------------------------------|------------------------------------|
| **数据处理**            | ✅ 单次运行 MapReduce 任务        | ✅ 每小时处理增量数据               |
| **系统维护**            | ✅ 手动触发日志清理               | ✅ 每日凌晨自动清理旧日志           |
| **测试任务**            | ✅ 运行一次集成测试               | ✅ 每晚定时执行回归测试             |
| **资源初始化**          | ✅ 初始化数据库或配置             | ❌ 无需重复执行                     |
| **周期性监控**          | ❌ 不适合                        | ✅ 每 5 分钟检查系统健康状态        |

---

### **4. 注意事项**

- **Job 的 Pod 重启策略**  
  Job 的 Pod 必须设置 `restartPolicy: Never` 或 `OnFailure`（不可用 `Always`），避免无限重启。
- **CronJob 的时区问题**  
  CronJob 默认使用 Kubernetes 控制平面节点的时区，若需指定时区，需在 Kubernetes 1.27+ 版本中配置 `timeZone` 字段。
- **资源泄漏风险**  
  - Job 完成后需手动清理或配置 `ttlSecondsAfterFinished` 自动删除。  
  - CronJob 应合理设置历史记录保留策略，避免存储过多旧 Job 对象。

---

### **5. 总结**

- **选择 Job**：当需要运行**一次性任务**（如数据处理、初始化操作），且任务完成后无需重复执行。  
- **选择 CronJob**：当需要按**固定时间表重复执行任务**（如定时备份、周期性报表生成）。  
- **组合使用**：CronJob 本质是通过生成 Job 来执行任务，两者可结合使用实现复杂调度逻辑。

在 Kubernetes 中，**Service** 是一个核心抽象，用于定义一组 Pod 的访问策略，提供稳定的网络端点、负载均衡和服务发现功能。它是解耦前端（客户端）和后端（Pod）的关键组件，尤其适用于动态变化的容器化环境。

---

### **1. Service 的作用**

- **稳定的网络标识**  
  解决 Pod IP 动态变化的问题，为 Pod 组提供固定访问入口（ClusterIP、DNS 名称等）。
- **负载均衡**  
  自动将流量分发到多个 Pod，支持多种负载均衡策略（如轮询、会话保持）。
- **服务发现**  
  通过 DNS 名称或环境变量，使应用能够动态发现后端服务。
- **流量控制**  
  支持定义访问端口映射、协议类型（TCP/UDP）等。

---

### **2. Service 的核心类型**

#### **(1) ClusterIP（默认类型）**

- **用途**：仅在集群内部访问服务（Pod 到 Pod 或内部组件间的通信）。
- **特点**：
  - 分配一个虚拟 IP（ClusterIP），生命周期内固定。
  - 通过 `kube-proxy` 实现内部负载均衡。
- **示例场景**：数据库服务仅允许集群内应用访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  type: ClusterIP
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306    # Service 暴露的端口
      targetPort: 3306  # Pod 监听的端口
```

---

#### **(2) NodePort**

- **用途**：通过节点 IP 和固定端口暴露服务，允许集群外部访问。
- **特点**：
  - 在集群所有节点上开放同一个端口（默认范围 30000-32767）。
  - 流量路径：外部请求 → 节点 IP:NodePort → Service → Pod。
- **示例场景**：开发测试环境临时暴露服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80       # Service 端口
      targetPort: 80 # Pod 端口
      nodePort: 31000 # 手动指定节点端口（可选）
```

---

#### **(3) LoadBalancer**

- **用途**：通过云提供商的负载均衡器（如 AWS ELB、GCP LB）暴露服务。
- **特点**：
  - 自动创建外部负载均衡器，并分配外部 IP。
  - 通常与 `NodePort` 和 `ClusterIP` 协同工作。
- **示例场景**：生产环境对外暴露高可用服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
    - protocol: TCP
      port: 443
      targetPort: 8080
```

---

#### **(4) Headless Service**

- **用途**：直接访问 Pod IP（无需负载均衡），适用于有状态应用（如 StatefulSet）。
- **特点**：
  - 设置 `clusterIP: None`，不分配 ClusterIP。
  - DNS 查询返回所有 Pod 的 IP 列表（或直接解析到单个 Pod）。
- **示例场景**：MySQL 主从集群中通过 Pod 域名直接访问特定实例。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
spec:
  clusterIP: None
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
```

---

### **3. 关键机制**

#### **(1) 标签选择器（Selector）**

- 通过 `selector` 字段匹配 Pod 的标签，动态维护后端端点（Endpoints）。
- **示例**：`selector: app: web` 会关联所有标签为 `app=web` 的 Pod。

#### **(2) kube-proxy 的流量转发**

- **iptables/IPVS 模式**：  
  `kube-proxy` 监听 Service 和 Endpoints 变化，动态配置节点上的流量转发规则。

#### **(3) DNS 解析**

- Service 的 DNS 名称格式：`<service-name>.<namespace>.svc.cluster.local`。
- 同一命名空间内的 Pod 可直接通过 `<service-name>` 访问。

---

### **4. 高级特性**

- **会话保持（Session Affinity）**  
  通过 `sessionAffinity: ClientIP` 将同一客户端的请求转发到固定 Pod。
- **多端口定义**  
  一个 Service 可暴露多个端口，适用于复杂协议（如 HTTP + gRPC）。
- **外部流量策略**  
  `externalTrafficPolicy: Local` 保留客户端源 IP，但可能导致流量不均衡。

---

### **5. 与其他组件的关系**

- **Ingress**  
  Service 通常与 Ingress 配合使用：  
  Ingress 定义外部访问规则（如域名、路径），并将流量转发到 Service。
- **EndpointSlices**  
  替代传统的 Endpoints 对象，提升大规模集群的性能。

---

### **6. 示例：完整请求流程**

1. 客户端访问 `web-service:80`（ClusterIP 类型）。
2. `kube-proxy` 通过 iptables/IPVS 规则将流量转发到后端 Pod。
3. 若 Pod 扩缩容，Service 自动更新 Endpoints，无需客户端感知。

---

### **7. 总结**

- **使用 Service 的场景**：
  - 需要为 Pod 组提供稳定访问入口。
  - 需负载均衡或服务发现。
  - 需隔离内部和外部流量（如 ClusterIP + Ingress）。
- **优势**：
  - 解耦服务提供方和消费方。
  - 适配 Pod 的动态生命周期。
  - 支持多云和混合云环境。

通过 Service，Kubernetes 实现了应用网络的抽象化，使开发者无需关注底层 Pod 的细节，专注于业务逻辑的实现。

在 Kubernetes 中，**LoadBalancer** 类型的 Service 是专为公有云环境设计的资源，通过与云提供商的负载均衡器（如 AWS ELB、GCP LB）集成，将集群内的服务暴露到外部网络。以下是其核心机制、配置方法及与云提供商集成的详细说明：

---

### **1. LoadBalancer Service 的核心机制**

- **自动创建外部负载均衡器**  
  当创建 `type: LoadBalancer` 的 Service 时，Kubernetes 会调用云提供商的 API，自动创建对应的负载均衡器（如 AWS 的 ELB、GCP 的 Cloud Load Balancing）。
- **外部 IP 分配**  
  云提供商为负载均衡器分配一个外部 IP 或 DNS 名称，供外部客户端访问。
- **流量转发路径**  
  外部流量 → 云负载均衡器 → Kubernetes 节点（NodePort）→ 目标 Pod。

---

### **2. 与云提供商负载均衡器的集成流程**

以 **AWS ELB** 和 **GCP LB** 为例：

#### **步骤 1：创建 LoadBalancer Service**

定义 Service 时指定 `type: LoadBalancer`，并关联后端 Pod 的标签选择器（`selector`）。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-web-service
spec:
  type: LoadBalancer
  selector:
    app: web  # 匹配 Pod 的标签
  ports:
    - protocol: TCP
      port: 80       # 负载均衡器监听端口
      targetPort: 80 # Pod 的端口
```

#### **步骤 2：云提供商自动创建负载均衡器**

- **AWS**：创建一个 Classic Load Balancer (CLB) 或 Application Load Balancer (ALB)，具体类型可通过注解配置。
- **GCP**：创建一个 TCP/UDP 网络负载均衡器或 HTTP(S) 负载均衡器。

#### **步骤 3：流量转发**

- 负载均衡器监听外部请求，并将流量转发到集群节点的 **NodePort**（由 Kubernetes 自动分配或手动指定）。
- `kube-proxy` 将 NodePort 流量路由到后端 Pod。

---

### **3. 云提供商特定配置（通过注解）**

不同云提供商支持通过 **annotations** 自定义负载均衡器的行为：

#### **(1) AWS 示例**

- **指定负载均衡器类型（ALB vs CLB）**：

  ```yaml
  metadata:
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-type: "external"
      service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
  ```

- **启用 SSL 终止**：

  ```yaml
  metadata:
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:us-west-2:123456789012:certificate/xxxxxx"
      service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
  ```

#### **(2) GCP 示例**

- **配置全局访问**：

  ```yaml
  metadata:
    annotations:
      networking.gke.io/load-balancer-type: "Internal"  # 内部负载均衡器
  ```

- **设置健康检查参数**：

  ```yaml
  metadata:
    annotations:
      cloud.google.com/load-balancer-type: "Regional"  # 区域级负载均衡
  ```

---

### **4. 高级配置选项**

#### **(1) 外部流量策略（`externalTrafficPolicy`）**

- **`Cluster`（默认）**  
  流量均匀分配到所有节点，但客户端源 IP 会被隐藏（NAT 转换）。
- **`Local`**  
  仅将流量转发到运行目标 Pod 的节点，保留客户端源 IP，但可能导致负载不均。

```yaml
spec:
  externalTrafficPolicy: Local
```

#### **(2) 保留客户端源 IP**

- 结合 `externalTrafficPolicy: Local` 使用，确保客户端 IP 不被丢失。
- 在云提供商负载均衡器中启用代理协议（如 AWS 需要配置注解）。

---

### **5. 示例：AWS 中创建 HTTPS 负载均衡器**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-https
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:us-west-2:123456789012:certificate/xxxxxx"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - name: https
      protocol: TCP
      port: 443
      targetPort: 80
```

---

### **6. 常见问题与排查**

#### **(1) 负载均衡器未创建**

- **检查点**：
  - 确认集群运行在支持的云环境中（如 AWS EKS、GCP GKE）。
  - 查看 Service 事件：`kubectl describe service <service-name>`。
  - 检查云账号权限是否允许创建负载均衡器。

#### **(2) 外部 IP 处于 Pending 状态**

- **可能原因**：
  - 云提供商配额不足（如 AWS ELB 数量限制）。
  - 安全组或防火墙规则阻止了负载均衡器的创建。

#### **(3) 健康检查失败**

- **解决方案**：
  - 确保 Pod 的 `readinessProbe` 和 `livenessProbe` 配置正确。
  - 检查负载均衡器的健康检查端口和路径是否与 Pod 匹配。

---

### **7. 总结**

- **适用场景**：  
  ✅ 需要将服务暴露到公网，且运行在公有云环境（AWS、GCP、Azure 等）。  
  ✅ 要求高可用性和自动扩缩容的外部流量入口。
- **优势**：  
  - 自动化集成云基础设施，减少手动配置。  
  - 提供企业级负载均衡能力（如 SSL 终止、WAF 集成）。  
- **注意事项**：  
  - 成本：云负载均衡器通常按使用量计费。  
  - 延迟：流量需经过云负载均衡器和节点转发，可能增加延迟。  

通过 LoadBalancer Service，Kubernetes 无缝对接云平台的高级网络功能，为生产环境提供可靠的外部服务暴露方案。

在 Kubernetes 中，**Service** 是一个核心抽象，用于定义一组 Pod 的访问策略，提供稳定的网络端点、负载均衡和服务发现功能。它是解耦前端（客户端）和后端（Pod）的关键组件，尤其适用于动态变化的容器化环境。

---

### **1. Service 的作用**

- **稳定的网络标识**  
  解决 Pod IP 动态变化的问题，为 Pod 组提供固定访问入口（ClusterIP、DNS 名称等）。
- **负载均衡**  
  自动将流量分发到多个 Pod，支持多种负载均衡策略（如轮询、会话保持）。
- **服务发现**  
  通过 DNS 名称或环境变量，使应用能够动态发现后端服务。
- **流量控制**  
  支持定义访问端口映射、协议类型（TCP/UDP）等。

---

### **2. Service 的核心类型**

#### **(1) ClusterIP（默认类型）**

- **用途**：仅在集群内部访问服务（Pod 到 Pod 或内部组件间的通信）。
- **特点**：
  - 分配一个虚拟 IP（ClusterIP），生命周期内固定。
  - 通过 `kube-proxy` 实现内部负载均衡。
- **示例场景**：数据库服务仅允许集群内应用访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  type: ClusterIP
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306    # Service 暴露的端口
      targetPort: 3306  # Pod 监听的端口
```

---

#### **(2) NodePort**

- **用途**：通过节点 IP 和固定端口暴露服务，允许集群外部访问。
- **特点**：
  - 在集群所有节点上开放同一个端口（默认范围 30000-32767）。
  - 流量路径：外部请求 → 节点 IP:NodePort → Service → Pod。
- **示例场景**：开发测试环境临时暴露服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80       # Service 端口
      targetPort: 80 # Pod 端口
      nodePort: 31000 # 手动指定节点端口（可选）
```

---

#### **(3) LoadBalancer**

- **用途**：通过云提供商的负载均衡器（如 AWS ELB、GCP LB）暴露服务。
- **特点**：
  - 自动创建外部负载均衡器，并分配外部 IP。
  - 通常与 `NodePort` 和 `ClusterIP` 协同工作。
- **示例场景**：生产环境对外暴露高可用服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
    - protocol: TCP
      port: 443
      targetPort: 8080
```

---

#### **(4) Headless Service**

- **用途**：直接访问 Pod IP（无需负载均衡），适用于有状态应用（如 StatefulSet）。
- **特点**：
  - 设置 `clusterIP: None`，不分配 ClusterIP。
  - DNS 查询返回所有 Pod 的 IP 列表（或直接解析到单个 Pod）。
- **示例场景**：MySQL 主从集群中通过 Pod 域名直接访问特定实例。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
spec:
  clusterIP: None
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
```

---

### **3. 关键机制**

#### **(1) 标签选择器（Selector）**

- 通过 `selector` 字段匹配 Pod 的标签，动态维护后端端点（Endpoints）。
- **示例**：`selector: app: web` 会关联所有标签为 `app=web` 的 Pod。

#### **(2) kube-proxy 的流量转发**

- **iptables/IPVS 模式**：  
  `kube-proxy` 监听 Service 和 Endpoints 变化，动态配置节点上的流量转发规则。

#### **(3) DNS 解析**

- Service 的 DNS 名称格式：`<service-name>.<namespace>.svc.cluster.local`。
- 同一命名空间内的 Pod 可直接通过 `<service-name>` 访问。

---

### **4. 高级特性**

- **会话保持（Session Affinity）**  
  通过 `sessionAffinity: ClientIP` 将同一客户端的请求转发到固定 Pod。
- **多端口定义**  
  一个 Service 可暴露多个端口，适用于复杂协议（如 HTTP + gRPC）。
- **外部流量策略**  
  `externalTrafficPolicy: Local` 保留客户端源 IP，但可能导致流量不均衡。

---

### **5. 与其他组件的关系**

- **Ingress**  
  Service 通常与 Ingress 配合使用：  
  Ingress 定义外部访问规则（如域名、路径），并将流量转发到 Service。
- **EndpointSlices**  
  替代传统的 Endpoints 对象，提升大规模集群的性能。

---

### **6. 示例：完整请求流程**

1. 客户端访问 `web-service:80`（ClusterIP 类型）。
2. `kube-proxy` 通过 iptables/IPVS 规则将流量转发到后端 Pod。
3. 若 Pod 扩缩容，Service 自动更新 Endpoints，无需客户端感知。

---

### **7. 总结**

- **使用 Service 的场景**：
  - 需要为 Pod 组提供稳定访问入口。
  - 需负载均衡或服务发现。
  - 需隔离内部和外部流量（如 ClusterIP + Ingress）。
- **优势**：
  - 解耦服务提供方和消费方。
  - 适配 Pod 的动态生命周期。
  - 支持多云和混合云环境。

通过 Service，Kubernetes 实现了应用网络的抽象化，使开发者无需关注底层 Pod 的细节，专注于业务逻辑的实现。

Kubernetes 中的 **Ingress** 用于管理外部访问集群内部服务的 **HTTP/HTTPS 流量**，充当集群的“智能路由网关”。它通过定义路由规则，将外部请求按域名、路径等条件分发到不同的后端服务，同时支持 TLS 加密等高级功能。以下是其核心作用及与外部流量的交互机制：

---

### **一、Ingress 的核心作用**

#### **1. 统一流量入口**

- **替代多个 LoadBalancer**  
  无需为每个服务创建独立的负载均衡器（节省云资源成本），通过单一入口（如一个公网 IP）承载多个服务的流量。
- **示例**：  
  通过 `api.example.com` 和 `app.example.com` 两个域名访问同一个集群的不同服务。

#### **2. 灵活的路由规则**

- **基于域名（Host）路由**  
  将不同域名的请求分发到对应的服务（如 `blog.example.com` → 博客服务，`api.example.com` → API 服务）。
- **基于路径（Path）路由**  
  同一域名下，按 URL 路径分发流量（如 `example.com/user` → 用户服务，`example.com/order` → 订单服务）。

#### **3. TLS 终止**

- **集中管理 HTTPS**  
  在 Ingress 层统一配置 SSL/TLS 证书，实现 HTTPS 加密访问，无需在后端服务中单独处理加密。
- **支持自动证书续签**  
  结合工具如 `cert-manager` 可自动申请和更新 Let's Encrypt 证书。

#### **4. 负载均衡与流量控制**

- **权重分流**  
  按比例将流量分配到不同版本的服务（如金丝雀发布）。
- **会话保持、限流、重试**  
  通过 Ingress 控制器扩展功能（如 Nginx 注解）。

---

### **二、Ingress 的工作原理**

#### **1. 核心组件**

- **Ingress 资源（API 对象）**  
  声明路由规则（YAML 文件定义域名、路径、后端服务等）。
- **Ingress 控制器（实际执行组件）**  
  监控 Ingress 资源变化，动态配置负载均衡器或反向代理（如 Nginx、Traefik、AWS ALB）。

#### **2. 工作流程**

1. **部署 Ingress 控制器**  
   安装如 Nginx Ingress Controller，它会自动创建一个 LoadBalancer 或 NodePort 类型的 Service，对外暴露入口。

2. **创建 Ingress 规则**  
   定义路由规则并关联后端 Service（ClusterIP 类型）。

3. **外部流量进入**  
   客户端通过 Ingress 控制器的外部 IP/DNS 发起请求。

4. **规则匹配与转发**  
   Ingress 控制器根据请求的域名和路径，将流量转发到对应的 Service，再由 Service 路由到 Pod。

![Ingress 流量示意图](https://d33wubrfki0l68.cloudfront.net/91ace2ec-843e-4b3d-acf4-5f5d5d3f77e5/859c663-01-ingress.svg)

---

### **三、Ingress 与外部流量的交互**

#### **1. 暴露 Ingress 控制器**

- **云环境（如 AWS/GCP）**  
  Ingress 控制器通常以 `LoadBalancer` 类型部署，云平台自动为其分配公网 IP。
- **本地环境**  
  使用 `NodePort` 或 `hostNetwork` 模式，通过节点 IP 和端口访问。

#### **2. DNS 配置**

- 将域名解析指向 Ingress 控制器的公网 IP（如 `A 记录` 或 `CNAME`）。

#### **3. 示例：完整请求路径**

1. 用户访问 `https://app.example.com`。
2. DNS 解析到 Ingress 控制器的公网 IP。
3. Ingress 控制器验证 TLS 证书并解密 HTTPS 流量。
4. 根据 `Host: app.example.com` 匹配 Ingress 规则，将请求转发到对应的 Service（如 `app-service:80`）。
5. Service 负载均衡到后端 Pod。

---

### **四、Ingress 配置示例**

#### **1. 定义 Ingress 规则**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /  # Nginx 特定注解（路径重写）
spec:
  tls:
  - hosts:
      - app.example.com
    secretName: tls-secret  # 引用存储证书的 Secret
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service  # 关联的后端 Service 名称
            port:
              number: 80
      - path: /static
        backend:
          service:
            name: static-service
            port:
              number: 80
```

#### **2. 创建 TLS 证书 Secret**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64 编码的证书>
  tls.key: <base64 编码的私钥>
```

---

### **五、常见 Ingress 控制器**

| 控制器                | 特点                                                                 |
|-----------------------|--------------------------------------------------------------------|
| **Nginx Ingress**     | 最常用，功能丰富，支持注解扩展（限流、重写等）。                         |
| **Traefik**           | 原生支持 Let's Encrypt，适合动态配置环境。                              |
| **AWS ALB Ingress**   | 直接集成 AWS ALB，适合云原生环境。                                     |
| **HAProxy Ingress**   | 高性能，适合需要极致吞吐量的场景。                                      |

---

### **六、Ingress vs. Service LoadBalancer**

| **特性**          | **Ingress**                          | **Service (LoadBalancer)**          |
|--------------------|--------------------------------------|-------------------------------------|
| **协议支持**       | HTTP/HTTPS                          | 任意 TCP/UDP                        |
| **路由粒度**       | 基于域名/路径                        | 仅端口级别                          |
| **成本效率**       | 单一入口承载多服务（节省公网 IP 和 LB） | 每个服务需独立 LB（成本高）           |
| **适用场景**       | 对外暴露 Web 服务                    | 非 HTTP 服务或需直接暴露 TCP 的场景   |

---

### **七、总结**

- **Ingress 的核心价值**：  
  ✅ 统一管理 HTTP/HTTPS 流量入口  
  ✅ 灵活的路由规则与 TLS 集中管理  
  ✅ 节省云资源成本  
- **使用场景**：  
  - 需要对外暴露多个 Web 服务（如微服务架构）。  
  - 实现灰度发布、A/B 测试等高级流量控制。  
  - 统一 HTTPS 证书管理。  

通过 Ingress，Kubernetes 能够以声明式的方式高效管理外部流量，是现代云原生应用不可或缺的组件。
