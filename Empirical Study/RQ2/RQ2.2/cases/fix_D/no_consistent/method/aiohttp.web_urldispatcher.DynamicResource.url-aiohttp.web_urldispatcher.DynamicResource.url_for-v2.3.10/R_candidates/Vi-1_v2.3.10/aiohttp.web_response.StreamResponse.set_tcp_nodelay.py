    def set_tcp_nodelay(self, value):
        payload_writer = self._payload_writer
        assert payload_writer is not None, \
            "Cannot set tcp_nodelay for not prepared response"
        payload_writer.set_tcp_nodelay(value)
