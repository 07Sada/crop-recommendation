import pymongo
import pandas as pd 
import json 
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class EnvironmentVariable:
    mongo_db_url=os.getenv('MONGO_URL')


env = EnvironmentVariable()

mongo_client = pymongo.MongoClient(env.mongo_db_url)

TARGET_COLUMN = 'label'
