def _assign_open_ports_to_workers(
    client: Client,
    host_to_workers: Dict[str, _HostWorkers]
) -> Dict[str, int]:
    """Assign an open port to each worker.

    Returns
    -------
    worker_to_port: dict
        mapping from worker address to an open port.
    """
    host_ports_futures = {}
    for hostname, workers in host_to_workers.items():
        n_workers_in_host = len(workers.all)
        host_ports_futures[hostname] = client.submit(
            _find_n_open_ports,
            n=n_workers_in_host,
            workers=[workers.default],
            pure=False,
            allow_other_workers=False,
        )
    found_ports = client.gather(host_ports_futures)
    worker_to_port = {}
    for hostname, workers in host_to_workers.items():
        for worker, port in zip(workers.all, found_ports[hostname]):
            worker_to_port[worker] = port
    return worker_to_port
