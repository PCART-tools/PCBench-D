def main():
    args = parse_args()
    benchmark_core.BenchmarkRunner(args).run()
