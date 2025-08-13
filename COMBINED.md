# 1Panel + Docker 一键部署 Dify 及RTSP视频帧捕获API服务

## 第一部分：RTSP视频帧捕获API服务

这是一个基于FastAPI的服务，可以通过API端点按需从RTSP流（如海康威视摄像头）中捕获视频帧。

### 系统要求

- Python 3.7+
- 依赖项见`requirements.txt`文件

### 配置说明

在运行服务前，您需要在`app.py`中配置您的摄像头：

1.  打开`app.py`文件
2.  找到`CAMERAS`字典
3.  编辑该字典，添加您的摄像头名称（作为键）和对应的RTSP地址（作为值）。例如：

    ```python
    CAMERAS = {
        "dzy": "rtsp://您的用户名:您的密码@摄像头IP1:554/stream1",
        "keting": "rtsp://您的用户名:您的密码@摄像头IP2:554/stream1",
    }
    ```

### 安装步骤

1.  安装依赖项：
    ```bash
    pip install -r requirements.txt
    ```

### 运行服务

在终端中运行以下命令：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### API接口说明

#### 按名称获取视频帧

-   `GET /get_frame_by_name?name=<摄像头名称>`
    -   从预配置的摄像头名称获取JPEG格式的视频帧
    -   **示例：** `http://localhost:8000/get_frame_by_name?name=dzy`

#### 按URL获取视频帧（旧版）

-   `GET /get_frame?rtsp_url=<RTSP地址>`
    -   从指定的RTSP流URL获取JPEG格式的视频帧
    -   **示例：** `http://localhost:8000/get_frame?rtsp_url=rtsp://admin:password@摄像头IP:554/Streaming/Channels/101`

---

## 第二部分：用 1Panel 在线安装 Docker（推荐）

> 适用于：Linux 服务器（CentOS 7/8、Ubuntu 18/20/22、Debian 10/11 等）
> 目的：先通过 1Panel 快速装好 Docker，再用官方 docker-compose 一键拉起 Dify，全程 5-10 分钟。

1. 以 **root** 身份登录服务器：
   ```bash
   sudo -i
   ```

2. 执行 1Panel 官方一键脚本：
   ```bash
   bash -c "$(curl -sSL https://resource.fit2cloud.com/1panel/package/v2/quick_start.sh)"
   ```

3. 按提示完成安装：
   - 默认会装最新稳定版 Docker & Docker-Compose；
   - 安装完成会打印类似：
     ```
     1Panel 访问地址：http://<服务器IP>:<端口>/<安全入口>
     用户名：admin
     密码：******
     ```

4. 浏览器打开上述地址，登录 1Panel 后台 → **容器** → **Docker** 即可图形化管理。

> 如果 Docker 安装失败，可单独执行备用脚本：
> ```bash
> bash <(curl -sSL https://linuxmirrors.cn/docker.sh)
> ```

### 使用 Dify 官方 Docker-Compose 部署

1. **回到服务器终端**，克隆官方仓库：
   ```bash
   git clone https://github.com/langgenius/dify.git
   cd dify/docker
   ```

2. 复制并编辑环境变量：
   ```bash
   cp .env.example .env
   # 按需修改 .env，如端口、密钥、模型配置等
   vim .env
   ```

3. 一键启动：
   ```bash
   docker compose up -d
   ```

4. 查看容器状态：
   ```bash
   docker compose ps
   ```
   所有容器状态为 `healthy` 即成功。

5. 浏览器访问：
   ```
   http://<服务器IP>:80
   ```
   首次打开会进入初始化向导，按提示创建管理员账号即可。

### 常用维护命令

| 操作 | 命令 |
|------|------|
| 停止 | `docker compose down` |
| 重启 | `docker compose restart` |
| 查看日志 | `docker compose logs -f` |
| 更新镜像 | `docker compose pull && docker compose up -d` |
| 卸载 | `docker compose down --remove-orphans && docker volume prune -f` |

### 云服务器额外注意

- **安全组**：放行 TCP 80（或自定义端口）
- **防火墙**：
  ```bash
  # CentOS 7/8
  firewall-cmd --permanent --add-port=80/tcp
  firewall-cmd --reload
  
  # Ubuntu/Debian
  ufw allow 80/tcp
  ```