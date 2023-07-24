import pymongo
import pandas as pd 
import json 
from dataclasses import dataclass
import os


@dataclass
class EnvironmentVariable:
    mongo_db_url=os.getenv('MONGO_DB_URL')


env = EnvironmentVariable()

mongo_client = pymongo.MongoClient(connect=env.mongo_db_url)

TARGET_COLUMN = 'label'
