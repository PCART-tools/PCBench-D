def _machines_to_worker_map(machines: str, worker_addresses: List[str]) -> Dict[str, int]:
    """Create a worker_map from machines list.

    Given ``machines`` and a list of Dask worker addresses, return a mapping where the keys are
    ``worker_addresses`` and the values are ports from ``machines``.

    Parameters
    ----------
    machines : str
        A comma-delimited list of workers, of the form ``ip1:port,ip2:port``.
    worker_addresses : list of str
        A list of Dask worker addresses, of the form ``{protocol}{hostname}:{port}``, where ``port`` is the port Dask's scheduler uses to talk to that worker.

    Returns
    -------
    result : Dict[str, int]
        Dictionary where keys are work addresses in the form expected by Dask and values are a port for LightGBM to use.
    """
    machine_addresses = machines.split(",")

    if len(set(machine_addresses)) != len(machine_addresses):
        raise ValueError(f"Found duplicates in 'machines' ({machines}). Each entry in 'machines' must be a unique IP-port combination.")

    machine_to_port = defaultdict(set)
    for address in machine_addresses:
        host, port = address.split(":")
        machine_to_port[host].add(int(port))

    out = {}
    for address in worker_addresses:
        worker_host = urlparse(address).hostname
        out[address] = machine_to_port[worker_host].pop()

    return out
