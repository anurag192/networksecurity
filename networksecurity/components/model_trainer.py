from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
import sys
import os

from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.entity.artifacts_entity import DataTransformedArtifact
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from networksecurity.utils.main_utils.utils import evaluate_models
import mlflow


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformedArtifact):
        self.model_trainer_config=model_trainer_config
        self.data_transformation_artifact=data_transformation_artifact

    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision score",precision_score)
            mlflow.log_metric("recall score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    



    def train_model(self,X_train,y_train,X_test,y_test):
        models={
            "LogisticRegression":LogisticRegression(),
            "KNeighborsClassifier":KNeighborsClassifier(),
            "DecisionTreeClassifier":DecisionTreeClassifier(),
            "AdaBoostClassifier":AdaBoostClassifier(),
            "RandomForestClassifier":RandomForestClassifier(),
            "GradientBoostingClassifier":GradientBoostingClassifier()

        }
        params={
            "DecisionTree":{
                'criterion':['gini','entropy','log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2']
            },
            "RandomForest":{
                'criterion':['gini','entropy','log_loss'],
                'max_features':['sqrt','log2'],
                'n_estimators':[8,16,32,64,128]
            },
            "GradientBoosting":{
                'loss':['log_loss','exponential_loss'],
                'learning_rate':[0.1,0.01,0.05,0.001],
                'subsample':[0.6,0.7,0.8,0.9,1],
                'criterion':['friedman_mse','squared_error'],
                'max_features':['auto','sqrt','log2'],
                'n_estimators':[8,16,32,64,128]
            },
            "LogisticRegression":{},
            "AdaboostClassifier":{
                'n_estimators':[8,16,32,64,128],
                'learning_rate':[0.1,0.01,0.001,0.05]

            }
        }
        model_report:dict=evaluate_models(X_train,y_train,X_test,y_test,models,params)
        best_model_score=max(sorted(model_report.values()))

        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        print(best_model_name)
        best_model=models[best_model_name]
        y_train_pred=best_model.predict(X_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred=best_model.predict(X_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        self.track_mlflow(best_model,classification_test_metric)
        
        preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        networkmodel=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=networkmodel)

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric)
        
        logging.info(f"Model trainer artifact:{model_trainer_artifact}")
        return model_trainer_artifact
        
    def initiate_model_train(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array(train_file_path)
            test_arr=load_numpy_array(test_file_path)

            

            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact=self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact

        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
        
