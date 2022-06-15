import json
import os
import os.path
import re
import json


def filter_text(text: str):
    new_text = re.sub(r'[^a-zA-Z]', '', text).lower()
    return new_text


def new_keyword(keyword):
    new_keyword = []
    for x in keyword:
        new_keyword.append(filter_text(x))
    return new_keyword


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'keyword')
    new_path = os.path.join(os.getcwd(), 'local', 'keyword')
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            data = json.load(f)
            f.close()
        data['keyword'] = new_keyword(data['keyword'])
        with open(os.path.join(new_path, filename), 'w') as f2:
            json.dump(data, f2)
