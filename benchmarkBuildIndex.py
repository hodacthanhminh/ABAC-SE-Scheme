from se.genkey import GenKey, read_key
import pandas as pd
from funmark import Benchmark
from se.buildindex import *

if __name__ == "__main__":
    # emails_df = pd.read_csv("./parsing_emails.csv",
    #                         converters={"keyword": lambda x: x.strip("[]").replace("'", "").split(", ")})
    emails_df = pd.read_json("./export_json.json")
    Data_benmark = [5, 10, 15, 20, 25, 30]
    SK = read_key("storage/256/key/key256-01.json")
    buildindex = BuildIndex(SK)
    bench = Benchmark()
    benchKey = Benchmark()
    export_bench = []


    def runBen(argv):
        df = argv[0]
        # number_doc = argv[1]
        df['encrypt_index'] = list(map(buildindex.main, df['keyword']))
        # export_df = pd.concat([df['file'], df["encrypt_index"]], axis=1, keys=['file', 'encrypt_index'])
        # export_df.to_json("./encrypt_{}.json".format(number_doc))
    for x in Data_benmark:
        number_doc = x*100
        random_df = emails_df.sample(n=number_doc)
        time, memory = bench.run(runBen, random_df, number_doc)
        number_keyword = buildindex.KeyWord
        buildindex.KeyWord = 0
        buildindex.Doc = 0
        bench.add(number_doc, time, memory)
        benchKey.add(number_keyword, time, memory)
        export_bench.append({'number_doc': number_doc, 'number_keyword': number_keyword,
                            'time': time, 'memory': memory})

    with open('bench_index.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(export_bench, ensure_ascii=False))
    plotObject = bench.plotTime(
        xlabel="n (x 1000)",
        ylabel="s",
        title="Build Index",
        show=True
    )
    plotObjectKey = benchKey.plotTime(
        xlabel="keyword",
        ylabel="s",
        title="Build Index Key",
        show=True)

    plotObject.savefig("buildIndex.png")
    plotObjectKey.savefig("buildIndexKey.png")
