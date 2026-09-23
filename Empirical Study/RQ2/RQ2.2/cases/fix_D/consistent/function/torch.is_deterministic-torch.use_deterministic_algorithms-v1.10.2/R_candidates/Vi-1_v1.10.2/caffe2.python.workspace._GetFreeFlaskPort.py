def _GetFreeFlaskPort():
    """Get a free flask port."""
    # We will prefer to use 5000. If not, we will then pick a random port.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    if result == 0:
        return 5000
    else:
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        # Race condition: between the interval we close the socket and actually
        # start a mint process, another process might have occupied the port. We
        # don't do much here as this is mostly for convenience in research
        # rather than 24x7 service.
        return port
