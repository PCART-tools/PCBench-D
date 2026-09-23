def benchmark_with_timer(fn, args, timer):
    timer(fn, args, 3)
    calibration = timer(fn, args, 1)
    iters = int(1.0 / calibration)
    return timer(fn, args, iters) / iters
