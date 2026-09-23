def _group_workers_by_host(worker_addresses: Iterable[str]) -> Dict[str, _HostWorkers]:
    """Group all worker addresses by hostname.

    Returns
    -------
    host_to_workers : dict
        mapping from hostname to all its workers.
    """
    host_to_workers: Dict[str, _HostWorkers] = {}
    for address in worker_addresses:
        hostname = urlparse(address).hostname
        if hostname not in host_to_workers:
            host_to_workers[hostname] = _HostWorkers(default=address, all=[address])
        else:
            host_to_workers[hostname].all.append(address)
    return host_to_workers
