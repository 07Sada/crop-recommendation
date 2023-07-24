import pandas as pd
from src.logger import logging
from src.exception import CropException
from src.config import mongo_client
import os
import sys
import numpy as np
import yaml
import dill


def get_collection_as_dataframe(database_name: str, collection_name: str) -> pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"{database_name} found in the mongodb")

        if "_id" in df.columns:
            logging.info("Dropping column: '_id'")
            df = df.drop(columns=["_id"], axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise CropException(e, sys)


def write_yaml_file(file_path, data: dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)

        with open(file_path, "w") as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
        raise CropException(e, sys)


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save objcet method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save objcet method of utils")
    except Exception as e:
        raise CropException(e, sys)
