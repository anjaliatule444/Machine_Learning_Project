from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from housing.constant import *
import os,sys
import pandas as pd
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    
    ## Check whether train and test file exists
    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Started Checking whether training and testing file exists at expected location")
            is_train_file_exist=False
            is_test_file_exist=False

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exist=os.path.exists(test_file_path)

            logging.info(f"train_file_exist=[{is_train_file_exist}] and test_file_exist=[{is_test_file_exist}] ")
            is_available= is_train_file_exist and is_test_file_exist

            if(is_available==False):
                message=f"Training file is not available at {self.data_ingestion_artifact.train_file_path} or Testing file is not available at {self.data_ingestion_artifact.test_file_path}"
                logging.info(message)
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_data_set_schema(self)->bool:
        try:
            validation_status=False

            ## Validate training and testing data set
            #1 .Number of columns
            #2. Check the values of ocean proximities(categorical variable)
            #3. Check column names

            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df

        except Exception as e:
            raise HousingException(e,sys) from e


    def get_and_save_data_drift_report(self):
        try:
            # Create object of Profile and pass sections parameter as data drift section.
            profile=Profile(sections=[DataDriftProfileSection()])

            ## Get train and test df
            train_df,test_df=self.get_train_and_test_df()

            ## Data Drift report
            profile.calculate(train_df,test_df)

            ## Save the report in json format using profile.json()
            ## profile.json return json object but when we want to load json in dict format then json.loads is used.
            report = json.loads(profile.json())

            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            ## Save the report in json format
            ##Indent=6 will increase the readability
            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            return report
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            # Create object of Dashboard and pass tabs parameter as DataDriftTab.
            dashboard=Dashboard(tabs=[DataDriftTab()])

            ## Get train and test df
            train_df,test_df=self.get_train_and_test_df()

            ## Data Drift report page
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir=os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)


            ## Save report page
            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e,sys) from e


    def is_data_drift_found(self):
        try:
            report=self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            ## Before starting data validation call function to check whether file exists
            self.is_train_test_file_exists()
            self.validate_data_set_schema()
            self.is_data_drift_found()
        
            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation Performed Successfully!!"
            )
            logging.info(f"Data Validation Artifact:[{data_validation_artifact}]")
        except Exception as e:
            raise HousingException(e,sys) from e