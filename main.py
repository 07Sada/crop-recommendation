from src.logger import logging
from src.exception import CropException
from src.utils import get_collection_as_dataframe
import os
import sys
from src.entity import config_entity
from src.components.data_ingestion import DataIngestion


def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # data Ingestion
        data_ingestion_config = config_entity.DataIngestionConfigData(training_pipeline_config = training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestioninitiat()

    except Exception as e:
        raise CropException(e, sys)
