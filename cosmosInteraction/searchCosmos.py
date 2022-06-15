# libs
import os
import sys
from os.path import dirname, join, realpath
from dotenv import load_dotenv
import pandas as pd
# class/funcs
parent_dir_name = dirname(dirname(realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env.prod')
load_dotenv(dotenv_path)
ENDPOINT = os.environ.get("ENDPOINT")
KEY = os.environ.get("KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
INDEX_CONTAINER = os.environ.get("INDEX_CONTAINER")

key_path = join(os.getcwd(), 'storage', '256', 'key', 'key256-01.json')

if __name__ == "__main__":
    from se.searchscheme import PSE
    from se.contants import d, L
    from cosmosMethod import CosmosClass
    cosmos_instance = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
    cosmos_instance.set_container(INDEX_CONTAINER)
    container = cosmos_instance.get_container()
    se = PSE(d, L)
    se.set_key(key_path)
    se.set_detail(True, True)
    words = input('Search for:').split(' ')
    se.insert_query(words)
    list_read = list(container.read_all_items(max_item_count=10))
    for x in list_read:
        index = pd.read_json(x['data'])
        se.set_index(index)
        se.set_search()
    result = se.get_result()
    print("[SEARCH MATH FILE]: ", result)
