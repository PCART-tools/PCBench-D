def _acquire_port() -> Tuple[_RemoteSocket, int]:
    s = _RemoteSocket()
    port = s.acquire()
    return s, port
