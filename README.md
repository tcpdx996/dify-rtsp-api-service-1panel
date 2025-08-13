# RTSP视频帧捕获API服务

这是一个基于FastAPI的服务，可以通过API端点按需从RTSP流（如海康威视摄像头）中捕获视频帧。

## 系统要求

- Python 3.7+
- 依赖项见`requirements.txt`文件

## 配置说明

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

## 安装步骤

1.  安装依赖项：
    ```bash
    pip install -r requirements.txt
    ```

## 运行服务

在终端中运行以下命令：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API接口说明

### 按名称获取视频帧

-   `GET /get_frame_by_name?name=<摄像头名称>`
    -   从预配置的摄像头名称获取JPEG格式的视频帧
    -   **示例：** `http://localhost:8000/get_frame_by_name?name=dzy`

### 按URL获取视频帧（旧版）

-   `GET /get_frame?rtsp_url=<RTSP地址>`
    -   从指定的RTSP流URL获取JPEG格式的视频帧
    -   **示例：** `http://localhost:8000/get_frame?rtsp_url=rtsp://admin:password@摄像头IP:554/Streaming/Channels/101`