import logging
import os
from datetime import datetime

# Create a folder for logs
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# Create log filename based on date
LOG_FILE = os.path.join(LOG_FOLDER, f"log_{datetime.now().strftime('%Y%m%d')}.log")

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
