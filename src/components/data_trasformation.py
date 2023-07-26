from src.entity import artifact_entity
from src.entity import config_entity
from src.logger import logging
from src.exception import CropException
from src import utils
from src.config import TARGET_COLUMN

from typing import Optional
import os
import sys

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: config_entity.DataTransformationConfig,
        data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
    ):
        try:
            logging.info(f"{'>'*20} Data Transformation Initiated {'<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise CropException(e, sys)

    @classmethod
    def get_data_tranformer_object(cls) -> Pipeline:
        try:
            standard_scaler = StandardScaler()

            pipeline = Pipeline(steps=[("StandardScaler", standard_scaler)])

            return pipeline

        except Exception as e:
            raise CropException(e, sys)

    def initiate_data_transformation(
        self,
    ) -> artifact_entity.DataTransformationArtifact:
        try:
            # reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # selecting input features for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            # selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # transformation on target column
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            # transforming input features
            transformation_pipeline = DataTransformation.get_data_tranformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipeline.transform(
                input_feature_train_df
            )
            input_feature_test_arr = transformation_pipeline.transform(
                input_feature_test_df
            )

            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            # save the numpy array
            utils.save_object(
                file_path=self.data_transformation_config.transformed_train_path,
                obj=train_arr,
            )
            utils.save_object(
                file_path=self.data_transformation_config.transformed_test_path,
                obj=test_arr,
            )

            utils.save_object(
                file_path=self.data_transformation_config.transform_object_path,
                obj=transformation_pipeline,
            )

            utils.save_object(
                file_path=self.data_transformation_config.target_encoder_path,
                obj=label_encoder,
            )

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path,
            )

            logging.info(f"Data transformation object : {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CropException(e, sys)
