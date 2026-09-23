    @property
    def tcp_nodelay(self):
        payload_writer = self._payload_writer
        assert payload_writer is not None, \
            "Cannot get tcp_nodelay for not prepared response"
        return payload_writer.tcp_nodelay
