def init_data_input_workers(
    net,
    input_blob_names,
    fetch_fun,
    batch_size,
    num_worker_threads=2,
    input_source_name="train",
    max_buffered_batches=800,
    init_fun=None,
    external_loggers=None,
    dont_rebatch=False,
    batch_columns=None,
    timeout=600
):
    global global_coordinator
    device_option = scope.CurrentDeviceScope()
    if (device_option is None):
        device_option = caffe2_pb2.DeviceOption(device_type=caffe2_pb2.CPU)

    metrics = Metrics(external_loggers)
    batch_feeder = BatchFeeder(
        net,
        input_blob_names,
        batch_size,
        device_option,
        scope.CurrentNameScope(),
        input_source_name,
        global_coordinator.get_queue(input_source_name, max_buffered_batches),
        metrics,
        dont_rebatch,
        batch_columns,
        timeout=timeout
    )

    # Launch fetch worker threads
    worker_ids = [
        global_coordinator.get_new_worker_id()
        for i in range(num_worker_threads)
    ]

    # Create coordinator object
    coordinator = WorkerCoordinator(
        input_source_name, worker_ids, init_fun, batch_feeder)

    workers = [
        threading.Thread(
            target=run_worker,
            name="data_workers fetcher id {}".format(worker_id),
            args=[coordinator,
                  DataWorker(coordinator, worker_id, fetch_fun, metrics,
                             batch_size, batch_feeder)],
        ) for worker_id in worker_ids
    ]

    workers.append(threading.Thread(
        target=enqueuer,
        name="Enqueuer {} {}".format(input_source_name, scope.CurrentNameScope()),
        args=[coordinator, batch_feeder]))
    coordinator._workers = workers
    global_coordinator.add(coordinator)

    return global_coordinator
