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

## Data Ingestion Related Variables
DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR="data_ingestion"    ## This is folder name which we dont have in config.yaml specified
DATA_INGESTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY="ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY="ingested_test_dir"

## Data Validation Related Variables
DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY="schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY="schema_dir"
DATA_VALIDATION_ARTIFACT_DIR_NAME="data_validation"
DATA_VALIDATION_REPROT_FILE_NAME_KEY="report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY="report_page_file_name"

## Data transformation related variables
DATA_TRANSFORMATION_ARTIFACT_DIR_NAME="data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY="add_bedroom_per_room"
DATA_TRANSFORMATION_DIR_NAME_KEY="transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY="transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_NAME_KEY="preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY="preprocessed_object_file_name"

COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"
NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"
TARGET_COLUMN_KEY="target_column"

