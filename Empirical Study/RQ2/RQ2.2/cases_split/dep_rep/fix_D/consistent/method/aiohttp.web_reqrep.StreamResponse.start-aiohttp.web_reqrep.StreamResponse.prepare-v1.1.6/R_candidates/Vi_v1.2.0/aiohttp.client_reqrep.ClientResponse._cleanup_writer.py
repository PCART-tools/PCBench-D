    def _cleanup_writer(self):
        if self._writer is not None and not self._writer.done():
            self._writer.cancel()
        self._writer = None
