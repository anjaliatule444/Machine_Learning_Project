import yaml
from housing.exception import HousingException
import os,sys
import numpy as np
import dill
from housing.constant import *
import pandas as pd

def read_yaml_file(file_path:str)->dict:
    ## Function to read yaml file and return it as dictionary
    try:
        config_info=None
        with open(file_path,"r") as yaml_file:
            config_info=yaml.safe_load(yaml_file)
        return config_info
    except Exception as e:
        raise HousingException(e,sys)

def save_numpy_array_data(file_path: str,array:np.array):
    """
    Save numpy array to file
    file_path: Path to save the file
    array: preprocessing object
    """
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        
    except Exception as e:
        raise HousingException(e,sys) from e

def load_numpy_array(file_path:str)->np.array:
    """
    load data as numpy array
    file_path: Path of file where preprocessing object is saved
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e


def save_object(file_path: str,obj):
    """
    Save pickle object to file
    file_path: Path to save the file
    """
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        
    except Exception as e:
        raise HousingException(e,sys) from e

def load_obj(file_path:str):
    """
    load data as pickle object
    file_path: Path of file where preprocessing object is saved
    """
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e

def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
    ## This function will load the file and convert the datatypes in accurate format i.e. numerical cols should have numeric datatype and categorical cols should have categorical type
    try:
        dataset_schema=read_yaml_file(schema_file_path)
        schema=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        dataframe=pd.read_csv(file_path)
        error_message=""
        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message=f"DataFrame column [{column}] is not in schema columns"
        if(len(error_message)>0):
            raise HousingException(error_message,sys)

        return dataframe

    except Exception as e:
        raise HousingException(e,sys) from e

