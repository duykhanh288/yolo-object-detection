import os
from pathlib import Path
import torch

ROOT = Path(os.environ.get("APP_ROOT", Path(__file__).resolve().parent))
DATA_DIR = ROOT / "data"
ART_DIR = ROOT / "artifacts"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Chỉ định trọng số YOLO11n
YOLO_WEIGHTS = os.environ.get("YOLO_WEIGHTS", str(ART_DIR / "detector" / "yolo11n.pt"))

ENABLED_MODELS = {
    m.strip() for m in os.environ.get("ENABLED_MODELS", "detector").split(",") if m.strip()
}

MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "8"))
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:8501").split(",")