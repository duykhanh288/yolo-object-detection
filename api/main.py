import base64
import io
import time
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, MAX_UPLOAD_MB
from core.detector import ObjectDetector

app = FastAPI(title="Object Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = ObjectDetector()

async def _read_image(file: UploadFile) -> Image.Image:
    data = await file.read()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"Ảnh vượt quá {MAX_UPLOAD_MB} MB")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
        return image.convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "File không phải ảnh hợp lệ (jpg, png, webp)")

def _to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

@app.post("/api/detect")
async def detect(file: UploadFile = File(...), conf: float = Form(0.25)):
    t0 = time.perf_counter()
    result, annotated = detector.detect(await _read_image(file), conf=min(max(conf, 0.05), 0.95))
    return {
        **result,
        "image": _to_base64(annotated),
        "latency_ms": round((time.perf_counter() - t0) * 1000, 1)
    }