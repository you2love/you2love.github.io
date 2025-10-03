# Kubernetes
<!-- toc --> 

## 1. YAML 文件基础结构

Kubernetes YAML文件通常包含以下顶级字段：

```yaml
apiVersion: <版本>  # 指定API版本
kind: <资源类型>    # 指定资源类型(Pod, Deployment, Service等)
metadata:          # 元数据
  name: <名称>
  labels:          # 标签
    key: value
spec:              # 资源规格定义
  # 资源特定配置
```

## 2. 核心组件详解

### 2.1 apiVersion

指定Kubernetes API版本，常见值包括：
- `v1` - 核心API组(Pod, Service, Node等)
- `apps/v1` - 工作负载API组(Deployment, StatefulSet等)
- `networking.k8s.io/v1` - 网络API组(Ingress等)
- `batch/v1` - 批处理API组(Job, CronJob等)

### 2.2 kind

定义资源类型，常见类型包括：
- 工作负载资源：Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob
- 服务发现：Service, Ingress
- 配置与存储：ConfigMap, Secret, PersistentVolume, PersistentVolumeClaim
- 策略：ResourceQuota, LimitRange
- 元数据：Namespace, Node

### 2.3 metadata

包含资源的元数据：
- `name`: 资源名称(在namespace内唯一)
- `namespace`: 命名空间(默认为default)
- `labels`: 键值对标签，用于选择器
- `annotations`: 键值对注释，用于非标识性元数据

### 2.4 spec

定义资源的期望状态，具体内容因资源类型而异。

## 3. 常见资源类型示例

### 3.1 Pod 示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

### 3.2 Deployment 示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
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
        image: nginx:latest
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 3.3 Service 示例

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP  # 或 NodePort, LoadBalancer
```

### 3.4 ConfigMap 示例

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: production
  config.json: |
    {
      "debug": false,
      "logging": "info"
    }
```

### 3.5 Secret 示例 (base64编码)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: dXNlcm5hbWU=  # "username"的base64编码
  password: cGFzc3dvcmQ=  # "password"的base64编码
```

## 4. 高级特性

### 4.1 探针(Probes)

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 20
readinessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 4.2 资源限制与请求

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "1"
    memory: "1Gi"
```

### 4.3 卷挂载

```yaml
volumes:
- name: config-volume
  configMap:
    name: app-config
- name: secret-volume
  secret:
    secretName: db-secret

containers:
- name: app
  volumeMounts:
  - name: config-volume
    mountPath: /etc/config
  - name: secret-volume
    mountPath: /etc/secrets
    readOnly: true
```

### 4.4 环境变量

```yaml
env:
- name: ENV_VAR
  value: "value"
- name: CONFIG_VAR
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: APP_COLOR
- name: SECRET_VAR
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: username
```

## 5. 最佳实践

1. **使用标签和选择器**：合理使用标签组织资源，便于管理和选择
2. **资源限制**：始终为容器设置资源请求和限制
3. **探针配置**：配置适当的存活和就绪探针
4. **配置与代码分离**：使用ConfigMap和Secret管理配置
5. **版本控制**：将YAML文件纳入版本控制系统
6. **模板化**：使用Helm或Kustomize管理复杂配置
7. **命名约定**：采用一致的命名约定(如`<应用名>-<环境>-<组件>`)
8. **最小权限**：遵循最小权限原则配置RBAC

## 6. 常见问题排查

1. **格式错误**：确保YAML格式正确(缩进、引号等)
2. **API版本不匹配**：检查集群支持的API版本
3. **资源不足**：检查节点资源是否足够
4. **镜像拉取失败**：检查镜像名称和拉取策略
5. **权限问题**：检查ServiceAccount和RBAC配置
6. **端口冲突**：确保服务端口不冲突
7. **选择器不匹配**：检查Deployment和Service的选择器是否一致

## 7. 工具推荐

1. **kubectl apply**：部署和更新资源
2. **kubectl diff**：查看变更差异
3. **kubeval**：验证YAML语法
4. **Helm**：包管理工具
5. **Kustomize**：原生Kubernetes配置管理
6. **yq**：YAML处理工具(类似jq)

通过合理编写和管理Kubernetes YAML文件，可以高效地部署和管理容器化应用，实现基础设施即代码(IaC)的实践。