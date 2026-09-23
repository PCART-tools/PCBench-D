def worker_set_affinity(_):
    os.sched_setaffinity(0, [multiprocessing.cpu_count() - 1])
