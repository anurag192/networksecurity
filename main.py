from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig

import os
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformed_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformed_artifact)

        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        logging.info("Model trainer config initialised")
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformed_artifact)
        logging.info("Model trainer initialised")
        model_trainer_artifact=model_trainer.initiate_model_train()
        logging.info("Model trainer artifact initialised")
        print(model_trainer_artifact)
        logging.info("Model Trainer Completed")

        






    except Exception as e:
        raise NetworkSecurityException(e,sys)
        











    except Exception as e:
        raise NetworkSecurityException(e,sys)
