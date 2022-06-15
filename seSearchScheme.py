# libs
import pandas as pd
import os
import json
import sys
import getopt
# se scheme
from se.searchscheme import PSE
from se.contants import d, L


def myfunc(argv):
    key_path = ""
    index_path = ""
    arg_help = "{0} -k <Key Path> -i <Index Path>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hk:i:", ["help", "keyPath=", "indexPath="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-k", "--keyPath"):
            key_path = arg
        elif opt in ("-i", "--indexPath"):
            index_path = arg
    return (key_path, index_path)


if __name__ == "__main__":
    (key_path, index_path) = myfunc(argv=sys.argv)
    scheme = PSE(d, L)
    scheme.set_key(key_path)
    basic_scheme = input('Basic search [y|N] ? :')
    and_search = input('Search with And Query [y|N] ? :')
    basic = basic_scheme.lower() == "y" or basic_scheme.lower() == "yes"
    andQ = and_search.lower() == "y" or and_search.lower() == "yes"
    scheme.set_detail(basic, andQ)
    words = input('Search for:').split(' ')
    scheme.insert_query(words)
    path = os.path.join(os.getcwd(), index_path)
    for x in os.listdir(path):
        with open(os.path.join(path, x), 'r') as f:
            file_data = json.load(f)
            df = pd.read_json(file_data['data'])
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
            path = "./storage/document/{}.json".format(file_read)
            with open(path, 'r') as f:
                print(json.load(f))
        except:
            print("File don't exits")
