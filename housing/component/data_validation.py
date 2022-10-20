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
from housing.util.util import read_yaml_file


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

    def validate_number_of_columns(self,schema_file_path,train_file_path,test_file_path)->bool:
        try:
            schema_info=read_yaml_file(schema_file_path)
            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            self.status=False

            no_of_cols_in_schema=len(schema_info["columns"])
            no_of_cols_in_train_df=len(train_df.columns)
            no_of_cols_in_test_df=len(test_df.columns)

            logging.info(f"Schema columns=[{no_of_cols_in_schema}] -- Train columns=[{no_of_cols_in_train_df}] --Test columns=[{no_of_cols_in_test_df}]")

            if(no_of_cols_in_schema==no_of_cols_in_train_df and no_of_cols_in_train_df==no_of_cols_in_test_df):
                self.status=True

            logging.info(f"Validate Number of Columns:[{self.status}]")
            return self.status
        except Exception as e:
            raise HousingException(e,sys) from e

    def check_domain_values_of_categorical_columns(self,schema_file_path,train_file_path,test_file_path):
        try:
            schema_info=read_yaml_file(schema_file_path)
            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            self.status=False

            unique_in_schema=len(schema_info["domain_value"]["ocean_proximity"])
            unique_in_train=len(train_df["ocean_proximity"].unique())
            unique_in_test=len(test_df["ocean_proximity"].unique())

            logging.info(f"Schema Unique=[{unique_in_schema}] -- Train Unique=[{unique_in_train}] --Test Unique=[{unique_in_test}]")

            if(unique_in_schema==unique_in_train and unique_in_train==unique_in_test):
                    self.status=True
            
            logging.info(f"Categorical column domain values:[{self.status}]")
            return self.status
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_names_of_columns(self,schema_file_path,train_file_path,test_file_path):
        try:
            schema_info=read_yaml_file(schema_file_path)
            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            self.status=False

            commons_between_train_and_test=len(train_df.columns.intersection(test_df.columns))
            commons_between_train_and_schema=len(train_df.columns.intersection(schema_info["columns"]))

            logging.info(f"Commons Between Train and Test=[{commons_between_train_and_test}] \n Commons Between Train and Schema=[{commons_between_train_and_schema}] ")

            if(commons_between_train_and_test==commons_between_train_and_schema):
                    self.status=True
            
            logging.info(f"Columns Identical:[{self.status}]")
            return self.status

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def validate_data_set_schema(self)->bool:
        try:
            validation_status=False

            schema_file_path=self.data_validation_config.schema_file_path
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            logging.info(f"Got Schema File Path:[{schema_file_path}]\n Train File Path:[{train_file_path}] \n Test File Path:[{test_file_path}]")

            ## Validate training and testing data set
            #1 .Number of columns
            status1=self.validate_number_of_columns(schema_file_path,train_file_path,test_file_path)

            #2. Check the values of ocean proximities(categorical variable)
            status2=self.check_domain_values_of_categorical_columns(schema_file_path,train_file_path,test_file_path)

            #3. Check column names
            status3=self.validate_names_of_columns(schema_file_path,train_file_path,test_file_path)

            if(status1==True and status2==True and status3==True):
                validation_status=True

            logging.info(f"Validation Status:[{validation_status}]")
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