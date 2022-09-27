import logging
from datetime import datetime
import os

## Folder for saving logs.
LOG_DIR="housing_logs"

##GET CURRENT TIMESTAMP
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

##Create log file
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

##Create log file directory
## exist_ok will work if this folder already exist
os.makedirs(LOG_DIR,exist_ok=True)

##Create file path
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s ',
    level=logging.INFO
)