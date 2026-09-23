def sweep(benchmark):
    # Synthesize the set of benchmarks to run.
    # This list contain tuples for ("string prefix", [rank...]).
    benchmarks = []

    def append_benchmark(prefix, ranks, opts=None):
        prefix = "%4d GPUs -- %s" % (len(ranks), prefix)
        benchmarks.append((prefix, ranks, opts))

    def local_print(msg):
        if dist.get_rank() == 0:
            print(msg, end='', flush=True)  # noqa: E999

    def print_header():
        local_print("\n")
        local_print("%22s" % "")
        for p in [50, 75, 90, 95]:
            local_print("%14s%10s" % ("sec/iter", "ex/sec"))
        local_print("\n")

    def print_measurements(prefix, nelem, measurements):
        measurements = sorted(measurements)
        local_print("%8s:" % prefix)
        for p in [50, 75, 90, 95]:
            v = np.percentile(measurements, p)
            local_print("  p%02d:  %1.3fs  %6d/s" % (p, v, nelem / v))
        local_print("\n")

    # Every process runs once by themselves to warm up (CUDA init, etc).
    append_benchmark("  warmup", [dist.get_rank()], {"use_ddp_for_single_rank": False})

    # Single machine baselines
    append_benchmark("  no ddp", range(1), {"use_ddp_for_single_rank": False})
    append_benchmark("   1M/1G", range(1))
    append_benchmark("   1M/2G", range(2))
    append_benchmark("   1M/4G", range(4))

    # Multi-machine benchmarks
    for i in range(1, (dist.get_world_size() // 8) + 1):
        append_benchmark("   %dM/8G" % i, range(i * 8))

    # Run benchmarks in order of increasing number of GPUs
    print_header()
    results = []
    for prefix, ranks, opts in sorted(benchmarks, key=lambda tup: len(tup[1])):
        # Turn range into materialized list.
        ranks = list(ranks)
        measurements = run_benchmark(benchmark, ranks, opts)
        if "warmup" not in prefix:
            print_measurements(prefix, benchmark.batch_size, measurements)
            results.append({"ranks": ranks, "measurements": measurements})

    return results
