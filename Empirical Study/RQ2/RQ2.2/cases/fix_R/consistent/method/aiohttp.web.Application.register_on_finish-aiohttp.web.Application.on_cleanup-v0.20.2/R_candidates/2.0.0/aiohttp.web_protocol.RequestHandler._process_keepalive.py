    def _process_keepalive(self):
        if self._force_close:
            return

        next = self._keepalive_time + self._keepalive_timeout

        # all handlers in idle state
        if len(self._request_handlers) == len(self._waiters):
            now = self._time_service.loop_time
            if now + 1.0 > next:
                self.force_close()
                return

        self._keepalive_handle = self._loop.call_at(
            next, self._process_keepalive)
