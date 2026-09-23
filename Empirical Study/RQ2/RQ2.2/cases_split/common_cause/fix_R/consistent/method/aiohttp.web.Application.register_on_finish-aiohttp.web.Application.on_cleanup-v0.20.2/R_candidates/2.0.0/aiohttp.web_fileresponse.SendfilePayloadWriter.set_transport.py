    def set_transport(self, transport):
        self._transport = transport

        if self._drain_waiter is not None:
            waiter, self._drain_maiter = self._drain_maiter, None
            if not waiter.done():
                waiter.set_result(None)
