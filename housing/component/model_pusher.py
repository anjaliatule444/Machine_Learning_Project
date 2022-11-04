from housing.entity.config_entity import ModelPusherConfig
from housing.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from housing.exception import HousingException
from housing.logger import logging
import os,sys
import shutil

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                    model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            logging.info(f"{'>>' * 30}Model Pusher log started.{'<<' * 30} ")
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def export_model(self)->ModelPusherArtifact:
        try:
            evaluation_model_file_path=self.model_evaluation_artifact.evaluated_model_path
            export_dir=self.model_pusher_config.export_dir_path
            model_name=os.path.basename(evaluation_model_file_path)
            export_model_file_path=os.path.join(export_dir,model_name)

            os.makedirs(export_dir, exist_ok=True)

            shutil.copy(src=evaluation_model_file_path, dst=export_model_file_path)
            ## We can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket so that the model will be available on cloud
            ## Thats how we deploy our model to the cloud
            logging.info(
                f"Trained model: {evaluation_model_file_path} is copied in export dir:[{export_model_file_path}]")

            model_pusher_artifact = ModelPusherArtifact(is_model_pushed=True,
                                                        export_model_file_path=export_model_file_path
                                                        )
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")