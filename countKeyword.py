import pandas as pd
import os
from os.path import join

root = os.getcwd()
keyword_path = join(root, "benchmark", "3000", "keyword")

if __name__ == "__main__":
    count = 0
    for filename in os.listdir(keyword_path):
        with open(join(keyword_path, filename), "r") as f:
            data = pd.read_json(f)
            count += data['keyword'].count()
    print(count)
