def init_workers(
    worker_fun,
    num_worker_threads=2,
    worker_name="train",
    init_fun=None,
    external_loggers=None,
    shutdown_fun=None,
):
    global global_coordinator

    metrics = Metrics(external_loggers)

    worker_ids = [
        global_coordinator.get_new_worker_id()
        for i in range(num_worker_threads)
    ]

    # Create coordinator object
    coordinator = WorkerCoordinator(
        worker_name, worker_ids, init_fun, shutdown_fun=shutdown_fun)

    # Launch fetch worker threads
    workers = [
        threading.Thread(
            target=run_worker,
            name="parallel_workers worker id {}".format(worker_id),
            args=[coordinator,
                  Worker(coordinator, worker_id, worker_fun, metrics)],
        ) for worker_id in worker_ids
    ]

    coordinator._workers = workers
    global_coordinator.add(coordinator)

    return global_coordinator
