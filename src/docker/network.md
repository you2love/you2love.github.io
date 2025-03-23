# network

Docker 网络是容器之间或容器与外部世界通信的核心机制。Docker 提供了多种网络模式，每种模式适用于不同的场景。以下是详细说明和实际示例：

---

## 一、Docker 默认网络模式

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

当 Docker 的 Bridge 网络（默认 `docker0` 网桥或自定义网桥）与宿主机的网络子网发生冲突时（例如 `docker0` 的默认子网 `172.17.0.0/16` 与宿主机局域网重叠），会导致容器无法访问外部网络或宿主机通信异常。以下是详细的排查和解决方法：

---

### 一、问题现象

- 容器无法访问宿主机局域网内的其他设备。
- 容器访问外网时出现超时或路由错误。
- 宿主机与容器之间的网络通信异常（如 `ping` 失败）。

---

### 二、原因分析

- **Docker 默认网段冲突**：  
  Docker 默认的 `docker0` 网桥使用 `172.17.0.0/16` 子网，若宿主机所在局域网也使用此网段，会导致路由混淆。
- **自定义网桥冲突**：  
  手动创建的 Bridge 网络子网与宿主机网络重叠。

---

### 三、解决方案

#### 方法 1：修改 Docker 默认网桥 `docker0` 的子网

**适用场景**：解决默认 `docker0` 网桥的冲突问题。

##### 步骤

1. **停止 Docker 服务**：  

   ```bash
   sudo systemctl stop docker
   ```

2. **删除现有网桥**：  

   ```bash
   sudo ip link set docker0 down
   sudo brctl delbr docker0
   ```

3. **修改 Docker 配置文件**：  
   编辑 `/etc/docker/daemon.json`（若文件不存在则新建），添加自定义子网配置：  

   ```json
   {
     "bip": "10.200.0.1/24",          # 指定 docker0 的 IP 和子网
     "default-address-pools": [
       {
         "base": "10.201.0.0/16",     # 自定义全局 IP 池范围
         "size": 24
       }
     ]
   }
   ```

   - `bip`：设置 `docker0` 的网关 IP 和子网（如 `10.200.0.1/24`）。
   - `default-address-pools`：定义 Docker 自动分配容器 IP 的地址池（避免与其他网络冲突）。

4. **重启 Docker 服务**：  

   ```bash
   sudo systemctl start docker
   ```

5. **验证新配置**：  

   ```bash
   docker network inspect bridge | grep Subnet
   ifconfig docker0                   # 查看新子网是否生效
   ```

---

#### 方法 2：创建自定义 Bridge 网络

**适用场景**：绕过默认 `docker0` 网桥，使用独立的子网。

##### 步骤

1. **创建自定义 Bridge 网络**：  

   ```bash
   docker network create \
     --driver bridge \
     --subnet 192.168.100.0/24 \     # 指定不冲突的子网
     --gateway 192.168.100.1 \
     my-custom-bridge
   ```

2. **运行容器并加入自定义网络**：  

   ```bash
   docker run -d --name my-container --network my-custom-bridge nginx
   ```

3. **验证容器网络**：  

   ```bash
   docker inspect my-container | grep IPAddress  # 查看容器 IP 是否在自定义子网内
   ```

---

#### 方法 3：调整宿主机网络（可选）

**适用场景**：如果宿主机网络可自由调整（如测试环境），可修改宿主机 IP 段。  
**操作示例**：  

```bash
# 修改宿主机网络为 10.0.0.0/24（需根据实际环境操作）
sudo nmcli con mod eth0 ipv4.addresses 10.0.0.100/24
sudo nmcli con up eth0
```

---

### 四、冲突排查工具

1. **查看宿主机网络接口**：  

   ```bash
   ip addr show           # 查看宿主机所有网卡及 IP 段
   route -n               # 查看路由表
   ```

2. **检查 Docker 网络配置**：  

   ```bash
   docker network ls
   docker network inspect bridge
   ```

3. **测试容器网络连通性**：  

   ```bash
   docker run --rm alpine ping 8.8.8.8          # 测试容器外网访问
   docker run --rm alpine ping 192.168.1.1      # 测试宿主机局域网访问
   ```

---

### 五、预防措施

1. **规划私有子网**：  
   - 使用非标准私有子网（如 `10.0.0.0/8`、`192.168.0.0/16` 中的冷门段）。
   - 避免与常见局域网（如家用路由器默认的 `192.168.1.0/24`）重叠。

2. **统一配置 Docker 地址池**：  
   在 `/etc/docker/daemon.json` 中全局配置：  

   ```json
   {
     "default-address-pools": [
       {
         "base": "10.100.0.0/16",    # 自定义全局 IP 池
         "size": 24
       }
     ]
   }
   ```

3. **使用 Docker Compose 显式定义网络**：  

   ```yaml
   # docker-compose.yml
   networks:
     app_net:
       driver: bridge
       ipam:
         config:
           - subnet: 172.22.0.0/24
   ```

---

### 六、典型案例

#### 场景：宿主机使用 `172.17.0.0/24` 导致与 `docker0` 冲突

1. **问题现象**：  
   - 容器无法访问宿主机所在局域网的设备。
   - 宿主机 `ping 172.17.0.1` 时得到响应（实际应为 `docker0` 网关）。

2. **解决步骤**：  
   - 修改 `/etc/docker/daemon.json`，设置 `"bip": "10.200.0.1/24"`。
   - 重启 Docker 并验证 `docker0` 子网已变更。

---

### 七、总结

通过修改 Docker 默认网桥子网或使用自定义 Bridge 网络，可有效解决子网冲突问题。关键步骤包括：  

1. **停止 Docker 服务**后清理旧配置。  
2. **修改 `/etc/docker/daemon.json`** 指定新子网。  
3. **创建自定义网络**并确保容器使用新网络。  
4. **验证路由和连通性**，确保容器与宿主机、外网通信正常。  

建议在生产环境中提前规划 Docker 网络架构，避免与现有网络环境冲突。
