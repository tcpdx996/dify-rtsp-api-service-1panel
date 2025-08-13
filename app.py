from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import io

app = FastAPI()

# 在这里配置全部摄像头名称和 RTSP 地址
# 建议名称使用拼音或英文，避免浏览器 URL 编码困扰
CAMERAS = {
    "大泊口水下": "rtsp://1.1.1.1:39888/wtFvX5BhhY5********",
    "客厅": "rtsp://admin:abc12345@192.168.3.29/Streaming/Channels/101",
    # 在这里可以添加更多摄像头，例如：
    # "houyuan": "rtsp://admin:password@camera-ip-3:554/Streaming/Channels/101",
}

def _capture_single_frame(rtsp_url: str):
    """从给定 RTSP 流捕获单帧并返回 JPEG 字节串。"""
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        cap.release()
        raise HTTPException(status_code=500, detail="无法打开 RTSP 流")

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise HTTPException(status_code=500, detail="无法捕获视频帧")

    ok, buffer = cv2.imencode(".jpg", frame)
    if not ok:
        raise HTTPException(status_code=500, detail="图片编码失败")

    return io.BytesIO(buffer.tobytes())


@app.get("/get_frame_by_name")
def get_frame_by_name(name: str = Query(..., description="摄像头名称，如 'dzy'")):
    """通过预设的摄像头名称获取视频帧。"""
    rtsp_url = CAMERAS.get(name)
    if rtsp_url is None:
        raise HTTPException(status_code=404, detail=f"未找到摄像头名称: {name}")

    image_stream = _capture_single_frame(rtsp_url)
    return StreamingResponse(image_stream, media_type="image/jpeg")


@app.get("/get_frame")
def get_frame(rtsp_url: str = Query(..., description="完整的 RTSP 地址")):
    """通过完整的 RTSP URL 获取视频帧 (保留此功能备用)。"""
    image_stream = _capture_single_frame(rtsp_url)
    return StreamingResponse(image_stream, media_type="image/jpeg")