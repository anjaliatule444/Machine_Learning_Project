from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_validation import DataValidation
from housing.component.data_ingestion import DataIngestion
from housing.component.data_transformation import DataTransformation

def main():
    try:
        pipeline_obj=Pipeline()
        pipeline_obj.start()
        #data_transformation_config=Configuration().get_data_transformation_config()
        #print(data_transformation_config)
        #file_path="E:\\Full stack data science-Python pratice\\Machine Learning\\Machine_Learning_Project\\housing\\artifact\\data_ingestion\\2022-10-22_13-08-18\\ingested_data\\train\\housing.csv"
        #schema_file_path="E:\\Full stack data science-Python pratice\\Machine Learning\\Machine_Learning_Project\\config\\schema.yaml"
        #df=DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
        #print(df.columns)
        #print(df.dtypes)
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
