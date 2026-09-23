    def _process_keepalive(self):
        if self._force_close or not self._keepalive:
            return

        next = self._keepalive_time + self._keepalive_timeout

        # handler in idle state
        if self._waiter:
            if self._loop.time() > next:
                self.force_close(send_last_heartbeat=True)
                return

        # not all request handlers are done,
        # reschedule itself to next second
        self._keepalive_handle = self._loop.call_later(
            self.KEEPALIVE_RESCHEDULE_DELAY, self._process_keepalive)
