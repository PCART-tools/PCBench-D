def time_cpu(fn, args, iters):
    s = time.perf_counter()
    for _ in range(iters):
        fn(*args)
    e = time.perf_counter()
    return e - s
