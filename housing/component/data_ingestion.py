from housing.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from housing.exception import HousingException
import os,sys
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'='*20}Data Ingestion Started.{'='*20} ")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def download_housing_data(self)-> str:
        try:

            # exctracting downlaod url for data download
            downlaod_url=self.data_ingestion_config.dataset_download_url

            # Get the folder location to download file
            tgz_download_dir=self.data_ingestion_config.tgz_download_dir

            ## Housing File name ie housing.tgz that we need to extract from downlaod url
            housing_file_name=os.path.basename(downlaod_url)

            ## Complete file path for download
            tgz_file_path=os.path.join(tgz_download_dir,housing_file_name)

            ## Create tgz_download_dir if already exist then delete it
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            os.makedirs(tgz_download_dir,exist_ok=True)

            ## download data from url at particular file location
            logging.info(f"Downloading file from :[{downlaod_url} at location :[{tgz_file_path}]")
            urllib.request.urlretrieve(downlaod_url,tgz_file_path)
            logging.info(f"Download completed for file :[{tgz_file_path}] successfully!")

            ## Return the file path where zip is stored
            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            ## Create directory for extracted data
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            ## Create directory-if exists already then remove it
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Exctracting tgz file :[{tgz_file_path}] into directory :[{raw_data_dir}]")
            ## Create tarfile object and extract zip file
            with tarfile.open(tgz_file_path) as housing_tgz_file_object:
                housing_tgz_file_object.extractall(raw_data_dir)
            logging.info(f"Extracted file in directory :[{raw_data_dir}] successfully !")
        
        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            ## All files in raw data dir will be displayed in form of list
            file_name=os.listdir(raw_data_dir)[0]

            ## Final Path of extracted file
            housing_file_path=os.path.join(raw_data_dir,file_name)

            ## read csv file
            logging.info(f"Reading CSV file :[{housing_file_path}]")
            housing_data_frame=pd.read_csv(housing_file_path)

            housing_data_frame["income_cat"]=pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0,1.5,3.0,4.5,6.0,np.inf],  ## 5 groups based on median income
                labels=[1,2,3,4,5]   ## 5 labels for 5 groups
            )

            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
            logging.info(f"Splittind data into train test data sets")
            ## income category ratio will be same in train and test
            for train_index,test_index in split.split(housing_data_frame,housing_data_frame["income_cat"]):
                strat_train_set=housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set=housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)
            
            ## Create train and test artifacts
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)
             
            ## Save the training data into training file
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir)
                strat_train_set.to_csv(train_file_path,index=False)
                logging.info(f"Saved training dataset successfully at location :[{train_file_path}]")
            
            ## Save the testing data into testing file
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir)
                strat_test_set.to_csv(test_file_path,index=False)
                logging.info(f"Saved test dataset successfully at location :[{test_file_path}]")

            ## initialize Data Ingestion Artifact Named Tuple
            data_ingestion_artifact=DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message=f"Data Ingestion Completed Successfully !!"
            )

            ## Return the artifact
            logging.info(f"Data Ingestion Artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact


        except Exception as e:
            raise Exception(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            ##Call the function for downloading data from url
            tgz_file_path =self.download_housing_data()

            ## call extract file function and pass zip file path to it
            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            ## call train test split function and return the output of train test split object
            return self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e
    
    ## Destructor
    def __del__(self):
        logging.info(f"Data Ingestion log Completed!.{'='*20}\n\n")