def benchmark_using_throughput_benchmark(config, module):
    print("Benchmarking via ThroughputBenchmark")
    bench = ThroughputBenchmark(module.module)
    bench.add_input(*module.tensor_inputs)
    stats = bench.benchmark(1, config.num_warmup_iters, config.num_iters)
    return stats.latency_avg_ms / NUM_LOOP_ITERS
