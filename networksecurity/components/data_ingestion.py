from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collect_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            print(df.columns)

            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            if "Unnamed: 0" in df.columns.to_list():
                df = df.drop(columns=["Unnamed: 0"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            feature_store_file_path = feature_store_file_path.replace(":", "_")
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_test_split(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            print(train_set.columns)
            logging.info("Performed train-test split")
            if "Unnamed: 0" in train_set.columns:
                train_set = train_set.drop(columns=["Unnamed: 0"])
            if "Unnamed: 0" in test_set.columns:
                test_set = test_set.drop(columns=["Unnamed: 0"])

            train_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_path=os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(test_path,exist_ok=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Exported train test split")


            

        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collect_as_dataframe()
            dataframe=self.export_data_to_feature_store(dataframe)
            self.train_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifact(train_data_path=self.data_ingestion_config.training_file_path,test_data_path=self.data_ingestion_config.test_file_path)
            return dataingestionartifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)