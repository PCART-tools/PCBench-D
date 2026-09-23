    def set_tcp_cork(self, value):
        payload_writer = self._payload_writer
        assert payload_writer is not None, \
            "Cannot set tcp_cork for not prepared response"

        payload_writer.set_tcp_cork(value)
