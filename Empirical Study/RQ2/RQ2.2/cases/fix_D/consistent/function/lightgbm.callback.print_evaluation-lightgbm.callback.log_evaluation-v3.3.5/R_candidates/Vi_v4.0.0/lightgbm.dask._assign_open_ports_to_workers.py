def _assign_open_ports_to_workers(
    client: Client,
    workers: List[str],
) -> Tuple[Dict[str, Future], Dict[str, int]]:
    """Assign an open port to each worker.

    Returns
    -------
    worker_to_socket_future: dict
        mapping from worker address to a future pointing to the remote socket.
    worker_to_port: dict
        mapping from worker address to an open port in the worker's host.
    """
    # Acquire port in worker
    worker_to_future = {}
    for worker in workers:
        worker_to_future[worker] = client.submit(
            _acquire_port,
            workers=[worker],
            allow_other_workers=False,
            pure=False,
        )

    # schedule futures to retrieve each element of the tuple
    worker_to_socket_future = {}
    worker_to_port_future = {}
    for worker, socket_future in worker_to_future.items():
        worker_to_socket_future[worker] = client.submit(operator.itemgetter(0), socket_future)
        worker_to_port_future[worker] = client.submit(operator.itemgetter(1), socket_future)

    # retrieve ports
    worker_to_port = client.gather(worker_to_port_future)

    return worker_to_socket_future, worker_to_port
