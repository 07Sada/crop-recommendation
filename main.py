from src.logger import logging
from src.exception import CropException
from src.utils import get_collection_as_dataframe
from src.entity import config_entity
from src.entity import artifact_entity
import sys
from src.components.data_ingestion import DataIngestion


if __name__=="__main__":
     try:
      training_pipeline_config = config_entity.TrainingPipelineConfig()

      data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
      data_ingestion_config.to_dict()

      data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
      data_ingestion.initiate_data_ingestion()

      print(f"Data Ingestion complete")
     
     except Exception as e:
          print(e)