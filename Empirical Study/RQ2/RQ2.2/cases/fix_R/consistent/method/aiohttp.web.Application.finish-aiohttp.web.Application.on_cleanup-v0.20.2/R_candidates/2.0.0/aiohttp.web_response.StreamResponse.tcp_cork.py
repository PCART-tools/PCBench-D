    @property
    def tcp_cork(self):
        payload_writer = self._payload_writer
        assert payload_writer is not None, \
            "Cannot get tcp_cork for not prepared response"
        return payload_writer.tcp_cork
