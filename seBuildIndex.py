# libs
import pandas as pd
import json
import os
import getopt
import sys
# se scheme
from se.genkey import read_key
from se.buildindex import BuildIndex
from se.buildindex import d


def myfunc(argv):
    key_path = ""
    key_id = ""
    out_dir = ""
    arg_help = "{0} -p <Key Path> -i <Key ID> -o <Out Dir> ".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hp:i:o:", ["help", "path=", "id=", "out="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-p", "--path"):
            key_path = arg
        elif opt in ("-i", "--id"):
            key_id = arg
        elif opt in ("-o", "--out"):
            out_dir = arg
    return (key_path, key_id, out_dir)


def genSearhFile(df: pd.Series, key_id: str, out_path: str):
    count = 0
    while len(df) > 0:
        export_df = df[:10]
        df = df[10:]
        count += 1
        data = {'id': 'index{}'.format(count), 'key': 'key{}'.format(
            key_id), 'data': export_df.to_json(orient='records')}
        with open(os.path.join(os.getcwd(), out_path, 'index-{}.json'.format(count)), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    (key_path, key_id, out_dir) = myfunc(sys.argv)
    full_keypath = os.path.join(key_path, "key{}.json".format(key_id))
    SK = read_key(full_keypath)
    buildindex = BuildIndex(SK)
    path = os.path.join(os.getcwd(), 'storage', 'keyword')
    data = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            data.append(json.load(f))
        f.close()
    df = pd.DataFrame(data, columns=['id', 'keyword'])
    df['encrypt_index'] = list(map(buildindex.main, df['keyword']))
    df = df.drop(columns=['keyword'])
    genSearhFile(df, key_id, out_dir)


# python3 seBuildIndex.py - p storage/256/key - i 256-01 storage/256/index
