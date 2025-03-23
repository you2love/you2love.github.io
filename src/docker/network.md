# network

Docker 网络是容器之间或容器与外部世界通信的核心机制。Docker 提供了多种网络模式，每种模式适用于不同的场景。以下是详细说明和实际示例：

---

### 一、Docker 默认网络模式

Docker 默认创建以下三种网络：

```bash
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
abc123...      bridge    bridge    local
def456...      host      host      local
ghi789...      none      null      local
```

---

### 二、核心网络模式及示例

#### 1. **Bridge 网络（默认模式）**

- **特点**：通过虚拟网桥（`docker0`）连接容器，默认分配私有 IP，容器间可通过 IP 或容器名通信。
- **适用场景**：单机多容器通信（默认隔离）。
- **示例**：

  ```bash
  # 1. 创建自定义 bridge 网络
  docker network create --driver bridge --subnet 172.18.0.0/16 my-bridge

  # 2. 运行两个容器并加入该网络
  docker run -d --name web --network my-bridge nginx
  docker run -it --name client --network my-bridge alpine

  # 3. 在 client 容器内测试连通性
  ping web  # 按容器名直接通信
  curl http://web
  ```

---

#### 2. **Host 网络**

- **特点**：容器直接使用宿主机的网络命名空间，无隔离，性能最佳。
- **适用场景**：高性能需求场景（如负载测试）。
- **示例**：

  ```bash
  # 运行容器使用 host 网络
  docker run -d --name nginx-host --network host nginx

  # 访问宿主机 IP 的 80 端口即可访问容器
  curl http://localhost
  ```

---

#### 3. **None 网络**

- **特点**：容器无网络接口，完全隔离。
- **适用场景**：安全测试或离线数据处理。
- **示例**：

  ```bash
  docker run -it --name no-net --network none alpine
  ifconfig  # 容器内仅能看到 lo 环回接口
  ```

---

#### 4. **Overlay 网络**

- **特点**：跨主机容器通信，基于 VXLAN 实现，用于 Docker Swarm 集群。
- **适用场景**：多主机容器组网（微服务集群）。
- **示例**：

  ```bash
  # 1. 初始化 Swarm 集群
  docker swarm init

  # 2. 创建 overlay 网络
  docker network create --driver overlay my-overlay

  # 3. 在 Swarm 中部署服务
  docker service create --name web --network my-overlay nginx
  docker service create --name client --network my-overlay alpine

  # 4. 在 client 服务中访问 web 服务
  docker exec -it client_container_id sh
  ping web  # 跨主机自动解析
  ```

---

#### 5. **Macvlan 网络**

- **特点**：为容器分配 MAC 地址，使其直接接入物理网络。
- **适用场景**：容器需要表现为物理设备（如 IoT 设备模拟）。
- **示例**：

  ```bash
  # 1. 创建 macvlan 网络
  docker network create -d macvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o parent=eth0 \
    my-macvlan

  # 2. 运行容器并指定静态 IP
  docker run -it --name macvlan-container \
    --network my-macvlan \
    --ip=192.168.1.100 \
    alpine
  ```

---

### 三、高级功能

#### 1. **端口映射**

将容器端口暴露到宿主机：

```bash
docker run -d -p 8080:80 --name nginx-port nginx
# 访问宿主机 IP:8080 即可访问容器 80 端口
```

#### 2. **DNS 自动解析**

同一自定义网络中的容器可通过名称通信：

```bash
docker run --net=my-bridge --name app1 my-app
docker run --net=my-bridge --name app2 my-app
# 在 app2 中可直接 ping app1
```

---

### 四、网络排查工具

- **查看容器 IP**：

  ```bash
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 容器名
  ```

- **进入容器测试网络**：

  ```bash
  docker exec -it 容器名 ping 目标IP
  ```

---

### 五、网络模式对比

| 模式       | 隔离性 | 性能  | 跨主机 | 典型场景             |
|------------|--------|-------|--------|----------------------|
| **Bridge** | 高     | 中等  | 否     | 单机多容器通信       |
| **Host**   | 无     | 最高  | 否     | 高性能需求           |
| **Overlay**| 高     | 中等  | 是     | Swarm 集群           |
| **Macvlan**| 中     | 高    | 是     | 容器直连物理网络     |

---

### 六、最佳实践

1. **优先使用自定义 Bridge 网络**，而非默认 `docker0`。
2. **生产环境避免使用 Host 网络**（安全风险）。
3. **跨主机通信首选 Overlay 网络**（Swarm/Kubernetes 集成）。

通过灵活组合这些模式，可以满足从开发到生产各种复杂场景的网络需求。
