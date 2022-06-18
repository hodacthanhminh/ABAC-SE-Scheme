from funmark import Benchmark
import json

if __name__ == "__main__":
    bench = Benchmark()
    benchKeyword = Benchmark()
    file = open("./bench_index.json", "r")
    array = json.load(file)
    file.close()
    for value in array:
        (number_doc, number_keyword, time, memory) = value.values()
        bench.add(number_doc, time, memory)
        benchKeyword.add(number_keyword, time, memory)

    plotObject = bench.plotTime(
        xlabel="n (x 100)",
        ylabel="s",
        title="Build Index",
        show=True
    )

    plotObjectKey = benchKeyword.plotTime(
        xlabel="keyword",
        ylabel="s",
        title="BuildIndex Keyword Amount",
        show=True)
