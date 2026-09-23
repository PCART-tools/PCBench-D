    def set_tcp_nodelay(self, value):
        value = bool(value)
        if self._tcp_nodelay == value:
            return
        if self._socket is None:
            return
        if self._socket.family not in (socket.AF_INET, socket.AF_INET6):
            return

        # socket may be closed already, on windows OSError get raised
        try:
            if self._tcp_cork:
                if CORK is not None:  # pragma: no branch
                    self._socket.setsockopt(socket.IPPROTO_TCP, CORK, False)
                    self._tcp_cork = False

            self._socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_NODELAY, value)
            self._tcp_nodelay = value
        except OSError:
            pass
