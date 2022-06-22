from ast import keyword
from se.genkey import GenKey, read_key
import pandas as pd
from funmark import Benchmark
from se.buildindex import *
import os
from os.path import join

number_doc = 1500

root = os.getcwd()
benchmark_folder = join(root, "benchmark", str(number_doc))
key_folder = join(root, "benchmark", "key", "key256.json")
index_folder = join(benchmark_folder, "index")
keyword_folder = join(benchmark_folder, "keyword")


def runBen(t):
    for x in os.listdir(keyword_folder):
        with open(join(keyword_folder, x), "r") as f:
            data = json.load(f)
            try:
                encrypt_index = buildindex.main(data['keyword'])
            except:
                pass
        f.close()


def runGen():
    data = []
    for file in os.listdir(keyword_folder):
        with open(os.path.join(keyword_folder, file), 'r') as f:
            data.append(json.load(f))
        f.close()
    df = pd.DataFrame(data, columns=['id', 'keyword'])
    df['encrypt_index'] = list(map(buildindex.main, df['keyword']))
    df = df.drop(columns=['keyword'])
    data = {'id': 'index'.format(number_doc), 'key': 'key256',
            'data': df.to_json(orient='records')}
    with open(join(index_folder, 'index{}.json'.format(number_doc)), 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


if __name__ == "__main__":
    SK = read_key(key_folder)
    buildindex = BuildIndex(SK)
    bench = Benchmark()
    benchKey = Benchmark()
    export_bench = []

    time, memory = bench.run(runBen)
    number_keyword = buildindex.KeyWord
    buildindex.KeyWord = 0
    buildindex.Doc = 0
    bench.add(number_doc, time, memory)
    benchKey.add(number_keyword, time, memory)
    export_bench.append({'number_doc': number_doc, 'number_keyword': number_keyword, 'time': time, 'memory': memory})

    with open(join(benchmark_folder, 'bench_index.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(export_bench, ensure_ascii=False))

    runGen()
