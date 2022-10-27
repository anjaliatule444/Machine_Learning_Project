from multiprocessing.connection import Pipe

from sklearn import preprocessing
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.config.configuration import Configuration
from housing.exception import HousingException
from housing.logger import logging
import os,sys
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from housing.constant import *
from housing.util.util import read_yaml_file,load_data,save_numpy_array_data,save_object


#   longitude: float
#   latitude: float
#   housing_median_age: float
#   total_rooms: float
#   total_bedrooms: float
#   population: float
#   households: float
#   median_income: float
#   median_house_value: float
#   ocean_proximity: category
#   income_cat: float


class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature
        except Exception as e:
            raise HousingException(e, sys) from e


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                        data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path
            dataset_schema=read_yaml_file(schema_file_path)
            numerical_columns=dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns=dataset_schema[CATEGORICAL_COLUMN_KEY]

            logging.info(f"Categorical Columns=[{categorical_columns}]")
            logging.info(f"Numerical Columns=[{numerical_columns}]")

            num_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="median")),
                ('feature_generator',FeatureGenerator(
                    add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                    columns=numerical_columns
                )),
                ('scaler',StandardScaler())
            ]
            )
            logging.info("Numerical Pipeline Created Successfully!")

            cat_pipeline=Pipeline(steps=[
                ('impute',SimpleImputer(strategy="most_frequent")),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ])
            logging.info("Categorical Pipeline Created Successfully!")
            
            preprocessing=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,categorical_columns)
            ])

            return preprocessing
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Data Transformation log Started!.{'='*20}\n\n")
            preprocessing_object=self.get_data_transformer_object()

            logging.info("Obtaining train and test file path.")
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            logging.info("Obtaining dataframes after load_data function execution.")
            schema_file_path=self.data_validation_artifact.schema_file_path
            train_df=load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)

            dataset_schema=read_yaml_file(file_path=schema_file_path)
            target_column_name=dataset_schema[TARGET_COLUMN_KEY]
            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            logging.info(f"Input Features Obtained->[{input_features_train_df}]")

            target_feature_train_df=train_df[[target_column_name]]
            logging.info(f"Target Feature Obtained->[{target_feature_train_df}]")

            input_features_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[[target_column_name]]

            input_feature_train_arr=preprocessing_object.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_object.transform(input_features_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            train_file_name=os.path.basename(transformed_train_dir).replace(".csv",".npz")
            test_file_name=os.path.basename(transformed_test_dir).replace(".csv",".npz")

            transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)
            preprocessing_object_file_path=self.data_transformation_config.preprocessed_object_file_path

            save_numpy_array_data(transformed_train_file_path,train_arr)
            logging.info(f"The train preproceesed numpy array saved successfully at [{transformed_train_file_path}]")

            save_numpy_array_data(transformed_test_file_path,test_arr)
            logging.info(f"The test preproceesed numpy array saved successfully at [{transformed_test_file_path}]")

            save_object(preprocessing_object_file_path,preprocessing_object)
            logging.info(f"The preproceesed object saved successfully at [{preprocessing_object_file_path}]")

            data_transformation_artifact=DataTransformationArtifact(
                is_transformed=True,
                message="Data Transformation Successful!!",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_object_file_path
            )

            logging.info(f"Data Transformation Artifact Created Successfully!-[{data_transformation_artifact}]")
            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    ## Destructor
    def __del__(self):
        logging.info(f"Data Transformation log Completed!.{'='*20}\n\n")