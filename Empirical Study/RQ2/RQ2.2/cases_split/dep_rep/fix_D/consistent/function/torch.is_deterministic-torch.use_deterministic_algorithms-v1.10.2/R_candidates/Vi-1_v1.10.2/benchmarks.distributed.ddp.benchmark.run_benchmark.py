def run_benchmark(benchmark, ranks, opts):
    group = dist.new_group(ranks=ranks, backend=benchmark.distributed_backend)
    measurements = []
    if dist.get_rank() in set(ranks):
        if not opts:
            opts = dict()
        measurements = benchmark_process_group(group, benchmark, **opts)
    dist.destroy_process_group(group)
    dist.barrier()

    # Aggregate measurements for better estimation of percentiles
    return list(itertools.chain(*allgather_object(measurements)))
