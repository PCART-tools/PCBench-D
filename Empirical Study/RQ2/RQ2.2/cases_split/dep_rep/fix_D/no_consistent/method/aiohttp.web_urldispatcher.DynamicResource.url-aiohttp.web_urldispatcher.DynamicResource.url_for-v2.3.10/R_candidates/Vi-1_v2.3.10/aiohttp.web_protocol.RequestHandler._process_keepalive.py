    def _process_keepalive(self):
        if self._force_close or not self._keepalive:
            return

        next = self._keepalive_time + self._keepalive_timeout

        # all handlers in idle state
        if len(self._request_handlers) == len(self._waiters):
            if self._loop.time() > next:
                self.force_close(send_last_heartbeat=True)
                return

        # not all request handlers are done,
        # reschedule itself to next second
        self._keepalive_handle = self._loop.call_later(
            self.KEEPALIVE_RESCHEDULE_DELAY, self._process_keepalive)
