# Compose
<!-- toc --> 

以下是 Docker Compose 配置文件的语法详解，以 YAML 格式为核心，按模块划分说明其功能和用法：

---

### **1. 文件结构概览**

```yaml
version: "3.8"        # 指定 Compose 文件格式版本
services:             # 定义所有容器服务
  service1:           # 服务名称（自定义）
    image: nginx      # 服务配置块
  service2:
    build: .
networks:             # 自定义网络定义
  my-network:
volumes:              # 数据卷定义
  my-volume:
```

---

### **2. `services` 核心配置项**

#### **基础配置**

| 字段 | 说明 | 示例 |
|------|------|------|
| `image` | 直接使用现成镜像 | `image: nginx:alpine` |
| `build` | 基于 Dockerfile 构建镜像 | `build: ./dir` 或带参数：<br>`build: <br>&nbsp; context: . <br>&nbsp; dockerfile: Dockerfile.prod` |
| `container_name` | 指定容器名称（默认随机生成） | `container_name: my-web` |
| `ports` | 端口映射（`宿主:容器`） | `- "80:80"`（精确）<br>`- "3000-3005:3000-3005"`（范围） |
| `expose` | 仅暴露端口给其他服务（不映射到宿主机） | `expose: ["5432"]` |

#### **环境变量**

| 字段 | 说明 | 示例 |
|------|------|------|
| `environment` | 直接定义环境变量 | `environment: <br>&nbsp; DB_HOST: db` |
| `env_file` | 从文件加载环境变量 | `env_file: .env` 或多个文件：<br>`env_file: <br>&nbsp; - common.env <br>&nbsp; - secrets.env` |

#### **持久化存储**

| 字段 | 说明 | 示例 |
|------|------|------|
| `volumes` | 挂载宿主机目录或数据卷 | `- /data:/var/lib/mysql`（绑定挂载）<br>`- db_data:/var/lib/mysql`（命名卷） |
| `volumes`（顶层） | 声明可复用数据卷 | `volumes: <br>&nbsp; db_data: <br>&nbsp;&nbsp; driver: local` |

#### **依赖控制**

| 字段 | 说明 | 示例 |
|------|------|------|
| `depends_on` | 服务启动顺序控制 | `depends_on: <br>&nbsp; - db <br>&nbsp; - redis` |
| `healthcheck` | 定义容器健康检查 | ```healthcheck: <br>&nbsp; test: ["CMD", "curl", "-f", "http://localhost"] <br>&nbsp; interval: 30s``` |

---

### **3. 网络配置 (`networks`)**

```yaml
services:
  web:
    networks:
      - frontend
      - backend

networks:
  frontend:           # 自定义网络1
    driver: bridge    # 网络驱动类型（默认bridge）
    ipam:             # IP地址管理
      config:
        - subnet: 172.28.0.0/16
  backend:            # 自定义网络2
    driver: overlay   # 适用于Swarm集群
    attachable: true
```

---

### **4. 数据卷配置 (`volumes`)**

```yaml
volumes:
  db_data:                   # 命名卷
    driver: local
    driver_opts:             # 驱动参数
      type: nfs
      o: addr=10.40.0.199,nfsvers=4
  metrics:                   # 外部已存在卷
    external: true
```

---

### **5. 扩展配置技巧**

#### **多环境配置合并**

```bash
# 同时加载基础配置 + 生产覆盖配置
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

#### **资源限制（生产环境必备）**

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          memory: 256M
```

#### **动态环境变量**

```yaml
ports:
  - "${HOST_PORT}:${CONTAINER_PORT}"  # 从.env文件或shell环境读取
```

---

### **6. 完整示例解析**

```yaml
version: "3.8"

services:
  webapp:
    build: 
      context: .
      args:
        NODE_ENV: production
    image: my-webapp:1.0
    ports:
      - "8080:3000"
    environment:
      - API_KEY=${API_KEY}  # 从.env文件读取
    volumes:
      - ./app:/code
      - logs:/var/log
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:6
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3
    volumes:
      - redis_data:/data

volumes:
  logs:
  redis_data:

networks:
  default:  # 默认网络配置
    driver: bridge
    ipam:
      config:
        - subnet: 172.22.0.0/24
```

---

### **7. 最佳实践**

1. **版本控制**：始终指定 `version` 字段（推荐 `3.8+`）
2. **敏感信息隔离**：使用 `.env` 文件管理密码/密钥
3. **健康检查**：关键服务必须配置 `healthcheck`
4. **资源限制**：生产环境明确设置 CPU/内存限制
5. **网络隔离**：不同服务组使用独立网络
6. **镜像管理**：优先使用固定版本标签（避免 `latest`）

---

### **常见错误排查**

1. **端口冲突**：使用 `docker compose ps` 查看占用情况
2. **卷权限问题**：Linux 需注意宿主机目录权限
3. **环境变量未生效**：检查 `.env` 文件路径和变量名大小写
4. **服务启动顺序问题**：依赖服务未配置健康检查导致超时

需要特定场景的语法细节说明，可以告诉我具体方向！ 💡
