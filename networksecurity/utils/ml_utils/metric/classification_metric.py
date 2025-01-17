from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,recall_score,precision_score
import os
import sys

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        f1_score_1=f1_score(y_true,y_pred)
        recall_score_1=recall_score(y_true,y_pred)
        precision_score_1=precision_score(y_true,y_pred)

        classification_metric_artifact=ClassificationMetricArtifact(
            f1_score=f1_score_1,
            recall_score=recall_score_1,
            precision_score=precision_score_1
        )
        return classification_metric_artifact


    except Exception as e:
        raise Exception(e,sys)

