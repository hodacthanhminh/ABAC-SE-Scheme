import os
import sys
import json
from os.path import join, dirname
from dotenv import load_dotenv

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
ENDPOINT = os.environ.get("ENDPOINT")
KEY = os.environ.get("KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
SEARCH_CONTAINER = os.environ.get("SEARCH_CONTAINER")

if __name__ == "__main__":
    from cosmosMethod import CosmosClass
    cosmos_instance = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
    cosmos_instance.set_container(SEARCH_CONTAINER)
    path = os.path.join(os.getcwd(), 'local', 'search')
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            json_data = json.load(f)
            f.close()
        cosmos_instance.create_document(json_data)
