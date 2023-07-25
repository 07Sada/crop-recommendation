from src.entity import config_entity
from src.entity import artifact_entity
from src.logger import logging
from src.exception import CropException
from src import utils

from typing import Optional
from sklearn.metrics import f1_score 
from sklearn.ensemble import RandomForestClassifier
import os
import sys

class ModelTrainer:

    def __init__(self, model_trainer_config: config_entity.ModelTrainerConfig,
                        data_transformation_artifact: artifact_entity.DataTransformationArtifact):

        try:
            logging.info(f"{'>'*30} Model Trainer Initiated {'<'*30}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise CropException(e, sys)

    
    def train_model(self, X, y):
        try:
            random_forest = RandomForestClassifier()
            random_forest.fit(X, y)
            
            return random_forest

        except Exception as e:
            raise CropException(e, sys)

    
    def initiate_model_trainer(self) -> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr. ")
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            logging.info(f"Training the model")
            model = self.train_model(X=X_train, y=y_train)

            logging.info(f"Calculating f1 train scrore")
            yhat_train = model.predict(X_train)
            f1_train_score = f1_score(y_true = y_train, y_pred = yhat_train, average="weighted")

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test, average="weighted")


            logging.info(f"train_score: {f1_train_score} and test score: {f1_test_score}")

            # checking for overfitting or underfitting or expected score
            logging.info(f"Checking if out model is underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                    expected accuracy: {self.model_trainer_config.expected_score}, model actual score: {f1_test_score}")

            logging.info(f"Checking if our model is overfitting or not")
            diff = abs(f1_train_score - f1_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} \
                    is more than overfitting threshold: {self.model_trainer_config.overfitting_threshold}")
            
            # save the trained model 
            logging.info(f"Saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score = f1_train_score, f2_test_score=f1_test_score)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise CropException(e, sys)
