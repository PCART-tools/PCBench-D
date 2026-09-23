    def set_tcp_cork(self, value):
        resp_impl = self._resp_impl
        if resp_impl is None:
            raise RuntimeError("Cannot set tcp_cork for "
                               "not prepared response")
        resp_impl.transport.set_tcp_cork(value)
