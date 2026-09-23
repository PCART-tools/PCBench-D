def clear_worker_pool():
    while not _WORKER_POOL.empty():
        _, result_file, _ = _WORKER_POOL.get_nowait()
        os.remove(result_file)

    if os.path.exists(SCRATCH_DIR):
        shutil.rmtree(SCRATCH_DIR)
