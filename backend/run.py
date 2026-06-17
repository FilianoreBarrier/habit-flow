import sys
from pathlib import Path

# Добавляем папку app в PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(APP_DIR))

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )