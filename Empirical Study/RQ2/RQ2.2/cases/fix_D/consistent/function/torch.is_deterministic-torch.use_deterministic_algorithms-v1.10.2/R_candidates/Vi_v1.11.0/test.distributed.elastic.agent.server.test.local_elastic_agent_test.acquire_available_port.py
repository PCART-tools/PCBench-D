def acquire_available_port():
    """
    Uses sockets to acquire an available port from the os for use.

    Note: To reduce the race condition where another process grabs the port
          after this function returns an available port, we should aim to use
          the port as quickly as possible.
    """
    addrs = socket.getaddrinfo(
        host="localhost",
        port=None,
        family=socket.AF_UNSPEC,
        type=socket.SOCK_STREAM
    )

    for addr in addrs:
        family, type, proto, _, _ = addr
        try:
            s = socket.socket(family, type, proto)
            s.bind(("localhost", 0))
            s.listen(0)
            port = s.getsockname()[1]
            s.close()
            return port
        except OSError as e:
            s.close()
            print(f"Socket creation attempt failed: {e}")

    raise RuntimeError("Failed to create a socket")
