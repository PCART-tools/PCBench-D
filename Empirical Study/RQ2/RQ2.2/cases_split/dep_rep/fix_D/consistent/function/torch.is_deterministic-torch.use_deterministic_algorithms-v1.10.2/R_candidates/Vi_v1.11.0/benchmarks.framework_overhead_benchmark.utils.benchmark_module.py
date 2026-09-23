def benchmark_module(config, module, use_throughput_benchmark=False):
    if use_throughput_benchmark:
        return benchmark_using_throughput_benchmark(config, module)
    module.forward(config.num_warmup_iters)
    print("Running module for {} iterations".format(config.num_iters))
    start = time.time()
    module.forward(config.num_iters)
    end = time.time()
    time_elapsed_s = (end - start)
    return (secs_to_ms(time_elapsed_s) / config.num_iters / NUM_LOOP_ITERS)
