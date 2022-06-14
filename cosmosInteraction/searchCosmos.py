# libs
import os
import sys
from os.path import dirname, join, realpath
from dotenv import load_dotenv
import pandas as pd
from cosmosInteraction.createEmailFile import EMAIL_CONTAINER
# class/funcs
from se.searchscheme import PSE
from se.contants import d, L

parent_dir_name = dirname(dirname(realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
ENDPOINT = os.environ.get("ENDPOINT")
KEY = os.environ.get("KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
SEARCH_CONTAINER = os.environ.get("SEARCH_CONTAINER")
EMAIL_CONTAINER = os.environ.get("EMAIL_CONTAINER")

if __name__ == "__main__":
    from cosmosMethod import CosmosClass
    cosmos_instance = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
    cosmos_instance.set_container(SEARCH_CONTAINER)
    container = cosmos_instance.get_container()
    list_read = list(container.read_all_items(max_item_count=5))
    key_id = input("Insert key_id")
    se = PSE(d, L, key_id)
    se.insert_query(basic=False)
    for x in list_read:
        index = pd.read_json(x['Data'])
        se.set_index(index)
        se.set_search()
    result = se.get_result()
    print("[SEARCH MATH FILE]: ", result)
    if len(result) == 0:
        exit()
    cosmos_instance.set_container(EMAIL_CONTAINER)
    doc_id = input("Read doc id:")
    data_respone = cosmos_instance.queryDocById(doc_id)
    print(data_respone[0]['content'])
