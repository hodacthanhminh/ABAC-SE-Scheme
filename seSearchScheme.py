# libs
import pandas as pd
import os
import json
# se scheme
from se.searchscheme import PSE
from se.contants import d, L


if __name__ == "__main__":
    scheme = PSE(d, L)
    scheme.insert_query()
    index_path = "./local/search/"
    for x in os.listdir(index_path):
        with open(index_path+x, 'r') as f:
            file_data = json.load(f)
            df = pd.read_json(file_data['Data'])
            f.close()
        scheme.set_index(df)
        scheme.set_search()
    result_items = scheme.get_result()
    print("Search file match:", result_items)
    if len(result_items) == 0:
        exit()
    while True:
        print("-------Input Exit to close------")
        file_read = input("Read file:")
        if (file_read == "Exit"):
            exit()
        try:
            path = "./local/email/{}.json".format(file_read)
            with open(path, 'r') as f:
                print(json.load(f))
        except:
            print("File don't exits")
