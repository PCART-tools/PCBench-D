def error_worker_init_fn(_):
    raise RuntimeError("Error in worker_init_fn")
