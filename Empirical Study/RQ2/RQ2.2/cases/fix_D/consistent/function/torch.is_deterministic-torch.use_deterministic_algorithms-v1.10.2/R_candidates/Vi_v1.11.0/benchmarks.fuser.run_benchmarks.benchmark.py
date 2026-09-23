def benchmark(fn, args):
    timer = time_cpu if args[0].device.type == "cpu" else time_cuda
    return benchmark_with_timer(fn, args, timer)
