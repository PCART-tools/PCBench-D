    def set_tcp_nodelay(self, value):
        resp_impl = self._resp_impl
        if resp_impl is None:
            raise RuntimeError("Cannot set tcp_nodelay for "
                               "not prepared response")
        resp_impl.transport.set_tcp_nodelay(value)
