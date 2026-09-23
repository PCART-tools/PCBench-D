    def _cleanup_writer(self):
        if self._writer is not None:
            self._writer.cancel()
        self._writer = None
        self._session = None
