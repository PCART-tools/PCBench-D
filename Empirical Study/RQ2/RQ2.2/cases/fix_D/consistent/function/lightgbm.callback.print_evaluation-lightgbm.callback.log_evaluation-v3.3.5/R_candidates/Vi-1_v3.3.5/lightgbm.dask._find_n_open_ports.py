def _find_n_open_ports(n: int) -> List[int]:
    """Find n random open ports on localhost.

    Returns
    -------
    ports : list of int
        n random open ports on localhost.
    """
    sockets = []
    for _ in range(n):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        sockets.append(s)
    ports = []
    for s in sockets:
        ports.append(s.getsockname()[1])
        s.close()
    return ports
