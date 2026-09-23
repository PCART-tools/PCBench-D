def get_free_port():
    sock = get_socket_with_port()
    with closing(sock):
        return sock.getsockname()[1]
