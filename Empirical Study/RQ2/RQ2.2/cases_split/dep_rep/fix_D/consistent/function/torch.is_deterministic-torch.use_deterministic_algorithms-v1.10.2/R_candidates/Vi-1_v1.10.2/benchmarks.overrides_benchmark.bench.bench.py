def bench(t1, t2):
    bench_times = []
    for _ in range(NUM_REPEAT_OF_REPEATS):
        time_start = time.time()
        for _ in range(NUM_REPEATS):
            torch.add(t1, t2)
        bench_times.append(time.time() - time_start)

    bench_time = float(torch.min(torch.tensor(bench_times))) / 1000
    bench_std = float(torch.std(torch.tensor(bench_times))) / 1000

    return bench_time, bench_std
