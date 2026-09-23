    def _start_cleanup_task(self):
        if self._cleanup_handle is None:
            now = self._loop.time()
            self._cleanup_handle = self._loop.call_at(
                ceil(now + self._keepalive_timeout), self._cleanup)
