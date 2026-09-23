def fill_core_pool(n: int):
    clear_worker_pool()
    os.makedirs(SCRATCH_DIR)

    # Reserve two cores so that bookkeeping does not interfere with runs.
    cpu_count = multiprocessing.cpu_count() - 2

    # Adjacent cores sometimes share cache, so we space out single core runs.
    step = max(n, 2)
    for i in range(0, cpu_count, step):
        core_str = f"{i}" if n == 1 else f"{i},{i + n - 1}"
        _, result_file = tempfile.mkstemp(suffix=".pkl", prefix=SCRATCH_DIR)
        _WORKER_POOL.put((core_str, result_file, n))
