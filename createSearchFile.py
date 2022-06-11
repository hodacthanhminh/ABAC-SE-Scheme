import os
import cosmosMethod as cm
import json

if __name__ == "__main__":
    endpoint = "https://azuredatabase2uit.documents.azure.com:443/"
    key = '6eOkaOakuyoI7KUAgIDvm0BpxxFJqPGqtWbiKamAAkVasqs7qKFr6dhqlbzISJwjJSC0MnuLUOsMZu4JwsaB4Q=='
    database_name = "EmailSearch"
    container_name = "search"
    cosmos_instance = cm.cosmos(endpoint, key, database_name)
    cosmos_instance.setContainer(container_name)
    for x in os.listdir('./search'):
        with open('./search/'+x) as fh:
            json_data = json.load(fh)
            cosmos_instance.createDocument(json_data)
