from genkey import *
import pandas as pd
import csv
from funmark import Benchmark
import timeit
from buildindex import *

if __name__ == "__main__":
    emails_df = pd.read_csv("./parsing_emails.csv",
                            converters={"keyword": lambda x: x.strip("[]").replace("'", "").split(", ")})
    Data_benmark = [5, 10, 15, 20, 25, 30]
    buildindex = BuildIndex(genkey.readFile())
    bench = Benchmark()
    benchKey = Benchmark()

    def runBen(argv):
        df = argv[0]
        number_doc = argv[1]
        start_timer = timeit.default_timer()
        df['encrypt_index'] = list(map(buildindex.main, df['keyword']))
        print(">> run timer: ", timeit.default_timer() - start_timer)
        export_df = pd.concat([df['file'], df["encrypt_index"]], axis=1, keys=['file', 'encrypt_index'])
        export_df.to_pickle("./encryptIndex_{}.csv".format(number_doc))

    for x in Data_benmark:
        number_doc = x*1000
        random_df = emails_df.sample(n=number_doc)
        time, memory = bench.run(runBen, random_df, number_doc)
        number_keyword = buildindex.KeyWord
        buildindex.KeyWord = 0
        buildindex.Doc = 0
        bench.add(number_doc, time, memory)
        benchKey.add(number_keyword, time, memory)

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
