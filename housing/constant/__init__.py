import os
from datetime import datetime

ROOT_DIR=os.getcwd() ## Get current working directory
CONFIG_DIR="config"  ## Get config Directory
CONFIG_FILE_NAME="config.yaml"   ## Get Config File Name 
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)  ## Join the variables together to form entire file path
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

## Training Pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY="artifact_dir"
TRAINING_PIPELINE_NAME_KEY="pipeline_name"