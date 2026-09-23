    @property
    def tcp_cork(self):
        resp_impl = self._resp_impl
        if resp_impl is None:
            raise RuntimeError("Cannot get tcp_cork for "
                               "not prepared response")
        return resp_impl.transport.tcp_cork
