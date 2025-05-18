import logging
from pathlib import Path
import shutil

UPLOAD_DIR = Path("/tmp/uploads")
RESULT_DIR = Path("/tmp/results")

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger("ml_service")

# Примитивная статистика
stats = {
    "requests_total": 0,
    "processing_time_total": 0.0
}

def log_request(filename: str):
    stats["requests_total"] += 1
    logger.info(f"📥 Новый файл: {filename}")

def log_result(filename: str, duration: float):
    stats["processing_time_total"] += duration
    logger.info(f"✅ Обработано: {filename} за {duration:.2f} сек")

def get_stats():
    total = stats["requests_total"]
    avg_time = stats["processing_time_total"] / total if total > 0 else 0
    return {
        "requests_total": total,
        "avg_processing_time_sec": round(avg_time, 3)
    }

def clear_tmp():
    try:
        deleted = 0
        for folder in [UPLOAD_DIR, RESULT_DIR]:
            for f in folder.glob("*"):
                if f.is_file():
                    f.unlink()
                    deleted += 1
                elif f.is_dir():
                    shutil.rmtree(f)
                    deleted += 1
        logger.info(f"🧹 Удалено временных файлов: {deleted}")
    except Exception as e:
        logger.error(f"Ошибка при очистке временных файлов: {e}")
