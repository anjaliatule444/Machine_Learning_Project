import yaml
from housing.exception import HousingException
import os,sys

def read_yaml_file(file_path:str)->dict:
    ## Function to read yaml file and return it as dictionary
    try:
        config_info=None
        with open(file_path,"r") as yaml_file:
            config_info=yaml.safe_load(yaml_file)
        return config_info
    except Exception as e:
        raise HousingException(e,sys)