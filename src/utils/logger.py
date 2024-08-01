import logging
from pathlib import Path
from datetime import datetime

log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file_name = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
log_file_path = log_dir / log_file_name

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

