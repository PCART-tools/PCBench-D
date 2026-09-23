def main():
    args = parse_args()

    benchmarks = [ALL_BENCHMARKS[name]() for name in args.benchmarks]
    for bench in benchmarks:
        bench.run()
    for bench in benchmarks:
        bench.display()
