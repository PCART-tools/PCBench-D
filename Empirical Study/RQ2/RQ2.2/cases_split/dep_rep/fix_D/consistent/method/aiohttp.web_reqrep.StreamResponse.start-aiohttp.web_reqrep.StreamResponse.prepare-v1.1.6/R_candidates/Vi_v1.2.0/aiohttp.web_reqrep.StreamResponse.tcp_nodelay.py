    @property
    def tcp_nodelay(self):
        resp_impl = self._resp_impl
        if resp_impl is None:
            raise RuntimeError("Cannot get tcp_nodelay for "
                               "not prepared response")
        return resp_impl.transport.tcp_nodelay
