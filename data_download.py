import opendatasets as od 
import os 
import json
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DATASET_URL = "https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset"

def create_kaggle_json_file():
    # Fetch the username and API key from the .env file
    username = os.getenv('username')
    key = os.getenv('key')

    kaggle_credentials = {
        "username": username,
        "key": key
    }

    # Path to the kaggle.json file
    kaggle_file_path = os.path.join(os.getcwd(), 'kaggle.json')

    # Write the dictionary to the .kaggle/kaggle.json file
    with open(kaggle_file_path, 'w') as file:
        json.dump(kaggle_credentials, file)

def remove_kaggle_json_file():
    # Path to the kaggle.json file
    kaggle_file_path = os.path.join(os.getcwd(), 'kaggle.json')

    # Remove the kaggle.json file
    os.remove(kaggle_file_path)

create_kaggle_json_file()

od.download(DATASET_URL)

# Remove the kaggle.json file after downloading the dataset
remove_kaggle_json_file()