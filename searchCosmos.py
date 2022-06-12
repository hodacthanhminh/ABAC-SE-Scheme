import numpy
import cosmosMethod as cm
import pandas as pd
from main import mainScheme
from CONSTANT import *

if __name__ == "__main__":
    endpoint = "https://azuredatabase2uit.documents.azure.com:443/"
    key = '6eOkaOakuyoI7KUAgIDvm0BpxxFJqPGqtWbiKamAAkVasqs7qKFr6dhqlbzISJwjJSC0MnuLUOsMZu4JwsaB4Q=='
    database_name = "EmailSearch"
    search_container = "search"
    email_container = "email"
    cosmos_instance = cm.cosmos(endpoint, key, database_name)
    cosmos_instance.setContainer(search_container)
    container = cosmos_instance.getContainer()
    list_read = list(container.read_all_items(max_item_count=5))
    se = mainScheme(d, L)
    se.insert_query(basic=False)
    for x in list_read:
        index = pd.read_json(x['Data'])
        se.set_index(index)
        se.set_search()
    result = se.get_result()
    print("[SEARCH MATH FILE]: ", result)
    if len(result) == 0:
        exit()
    cosmos_instance.setContainer(email_container)
    doc_id = input("Read doc id:")
    data_respone = cosmos_instance.queryDocById(doc_id)
    print(data_respone[0]['content'])
