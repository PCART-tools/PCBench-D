    def set_transport(self, transport):
        self._transport = transport

        chunk = b''.join(self._buffer)
        if chunk:
            transport.write(chunk)
            self._buffer.clear()

        if self._drain_waiter is not None:
            waiter, self._drain_waiter = self._drain_waiter, None
            if not waiter.done():
                waiter.set_result(None)
