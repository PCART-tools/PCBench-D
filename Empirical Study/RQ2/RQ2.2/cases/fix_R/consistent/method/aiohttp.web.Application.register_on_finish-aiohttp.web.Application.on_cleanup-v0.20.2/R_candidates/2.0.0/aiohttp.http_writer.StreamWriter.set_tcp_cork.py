    def set_tcp_cork(self, value):
        value = bool(value)
        if self._tcp_cork == value:
            return
        if self._socket is None:
            return
        if self._socket.family not in (socket.AF_INET, socket.AF_INET6):
            return

        try:
            if self._tcp_nodelay:
                self._socket.setsockopt(
                    socket.IPPROTO_TCP, socket.TCP_NODELAY, False)
                self._tcp_nodelay = False
            if CORK is not None:  # pragma: no branch
                self._socket.setsockopt(socket.IPPROTO_TCP, CORK, value)
                self._tcp_cork = value
        except OSError:
            pass
