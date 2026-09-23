    def _send_heartbeat(self):
        if self._heartbeat is not None and not self._closed:
            self.ping()

            if self._pong_response_cb is not None:
                self._pong_response_cb.cancel()
            self._pong_response_cb = call_later(
                self._pong_not_received, self._pong_heartbeat, self._loop)
