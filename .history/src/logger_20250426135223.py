import logging
import os
from datetime import datetime
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)
LOG_FILE = os.path.join(LOG_FOLDER, f"log_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
