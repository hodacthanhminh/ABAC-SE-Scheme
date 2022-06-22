import pandas as pd
import json
import sys
import os.path
import os  


def exportKeyword(keyword,index,content):
    root = os.getcwd()
    doc_path = os.path.join(root,"benchmark","3000","doc")
    kw_path = os.path.join(root, "benchmark","3000", "keyword")
    data_keyword = {"id": "document{}".format(index), "keyword": keyword}
    data_doc = {"id": "document{}".format(index), "content": content}
    with open(os.path.join(kw_path, "keyword{}.json".format(index)), "w") as f:
        json.dump(data_keyword,f)
        f.close()
    with open(os.path.join(doc_path, "document{}.json".format(index)), "w") as fD:
        json.dump(data_doc, fD)
        fD.close()
    # export_df = pd.concat([df['file'], df["encrypt_index"]], axis=1, keys=['file', 'encrypt_index'])
    # export_df.to_json("./benchmark/keyword/keyword-{}.json".format(df.index))


if __name__ == "__main__":
    emails_df = pd.read_json("./export_json.json")
    df = emails_df.sample(n=3000)
    list(map(exportKeyword,df['keyword'],df.index,df['content']))