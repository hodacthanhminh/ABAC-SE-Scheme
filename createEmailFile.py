from matplotlib import container
import pandas as pd
import json
import cosmosMethod as cm


if __name__ == '__main__':
        
    endpoint = "https://azuredatabase2uit.documents.azure.com:443/"
    key = '6eOkaOakuyoI7KUAgIDvm0BpxxFJqPGqtWbiKamAAkVasqs7qKFr6dhqlbzISJwjJSC0MnuLUOsMZu4JwsaB4Q=='
    database_name = "EmailSearch"
    container_name = "email"
    cosmos_instance = cm.cosmos(endpoint,key,database_name)
    cosmos_instance.changeContainer(container_name)
    df = pd.read_json("./export_json.json", orient="records")
    df = df.rename(columns={'ID':'id'})
    upload_df = df.sample(n=200)
    upload_df.to_json("./upload_email.json",orient="records")
    for i in upload_df.index:
        data = upload_df.loc[i].to_json()
        json_data = json.loads(data)
        cosmos_instance.createDocument(json_data)