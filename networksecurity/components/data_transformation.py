import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifacts_entity import (DataTransformedArtifact,DataValidationArtifact)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_object
from networksecurity.utils.main_utils.utils import save_numpy_array_data

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):

        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            df=pd.read_csv(file_path)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(cls)->KNNImputer:
        logging.info("Enter get data transformation method of transformation class")
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor:Pipeline=Pipeline([(
               "imputer" ,imputer
            )])
            return preprocessor


        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
        
    def initiate_data_transformation(self)->DataTransformedArtifact:
        logging.info("Initiate data transformation")

        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)

            

            target_feature_train_df=train_df[TARGET_COLUMN].replace(-1,0)
            target_feature_test_df=test_df[TARGET_COLUMN].replace(-1,0)
            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train=preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test=preprocessor_object.transform(input_feature_test_df)

            train_array=np.c_[transformed_input_feature_train,np.array(target_feature_train_df)]
            test_array=np.c_[transformed_input_feature_test,np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_array)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_array)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            data_transformed_artifact=DataTransformedArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformed_artifact




        except Exception as e:
            raise NetworkSecurityException(e,sys)


        