from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.exception import HousingException
from housing.logger import logging
from housing.util.util import write_yaml_file,read_yaml_file,load_obj,load_data
from housing.constant import *
from housing.component.model_trainer import evaluate_regression_model
import os,sys
import numpy as np

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                        data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_artifact:DataValidationArtifact,
                        model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.model_evaluation_config=model_evaluation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_best_model(self):
        try:
            model=None
            model_eval_file_path=self.model_evaluation_config.model_evaluation_file_path

            logging.info(f"Model Evaluation File Path:[{model_eval_file_path}]")
            if not os.path.exists(model_eval_file_path):
                write_yaml_file(file_path=model_eval_file_path)
                logging.info("Running pipeline for 1st time so model evaluation file created newly!")
                return model

            model_eval_file_content=read_yaml_file(model_eval_file_path)

            model_eval_file_content=dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                logging.info("best_model key is not avaliable in model_evaluation.yaml file content.")
                return model

            model=load_obj(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            logging.info(f"Model :[{model}]")
            return model
        except Exception as e:
            raise HousingException(e,sys) from e

    def update_evaluation_report(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            eval_file_path=self.model_evaluation_config.model_evaluation_file_path
            eval_file_content=read_yaml_file(file_path=eval_file_path)
            eval_file_content=dict() if eval_file_content is None else eval_file_content

            previous_best_model=None
            if BEST_MODEL_KEY in eval_file_content:
                previous_best_model=eval_file_content[BEST_MODEL_KEY]

            eval_result={
                BEST_MODEL_KEY:{
                    MODEL_PATH_KEY:model_evaluation_artifact.evaluated_model_path
                }
            }
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in eval_file_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    eval_file_content[HISTORY_KEY].update(model_history)

            eval_file_content.update(eval_result)
            logging.info(f"Updated Evaluation Content:[{eval_file_content}]")
            write_yaml_file(file_path=eval_file_path,data=eval_file_content)
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            trained_model_object_file_path=self.model_trainer_artifact.trained_model_file_path
            logging.info(f"Trained Model File Path:[{trained_model_object_file_path}]")
            trained_model_obj=load_obj(trained_model_object_file_path)

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            schema_file_path=self.data_validation_artifact.schema_file_path

            train_df=load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            logging.info(f"Train df with Target column:[{train_df}]")
            test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)
            logging.info(f"Test df with Target column:[{test_df}]")

            schema_content=read_yaml_file(schema_file_path)
            target_column_name=schema_content[TARGET_COLUMN_KEY]

            train_target_df=train_df[target_column_name]
            test_target_df=test_df[target_column_name]

            train_target_arr=np.array(train_target_df)
            logging.info(f"Train target array:[{train_target_arr}]")
            test_target_arr=np.array(test_target_df)
            logging.info(f"Test Target array:[{test_target_arr}]")

            train_df.drop(target_column_name,axis=1,inplace=True)
            logging.info(f"Train df without Target column:[{train_df}]")
            test_df.drop(target_column_name,axis=1,inplace=True)
            logging.info(f"Test df with Target column:[{test_df}]")

            model=self.get_best_model()

            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_object_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
                return model_evaluation_artifact
            
            model_list=[model,trained_model_obj]

            metric_info_artifact=evaluate_regression_model(model_list=model_list,
                                                            X_train=train_df,
                                                            X_test=test_df,
                                                            y_train=train_target_arr,
                                                            y_test=test_target_arr,
                                                            base_accuracy=self.model_trainer_artifact.model_accuracy)

            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_object_file_path)
                logging.info(response)
                return response

            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_object_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_object_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    ## Destructor
    def __del__(self):
        logging.info(f"Model Evaluation log Completed!.{'='*20}\n\n")
            


