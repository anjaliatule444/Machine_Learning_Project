from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_validation import DataValidation
from housing.component.data_ingestion import DataIngestion

def main():
    try:
        pipeline_obj=Pipeline()
        pipeline_obj.run_pipeline()
        #data_validation_config=Configuration().get_data_validation_config()
        #print(data_validation_config)
        '''
        config=Configuration()
        ingestion_obj=DataIngestion(config.get_data_ingestion_config())
        ingestion_artifact=ingestion_obj.initiate_data_ingestion()
        data_validation_config=config.get_data_validation_config()
        data_validation=DataValidation(data_validation_config,ingestion_artifact)
        print(data_validation.is_train_test_file_exists())
        '''
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()
