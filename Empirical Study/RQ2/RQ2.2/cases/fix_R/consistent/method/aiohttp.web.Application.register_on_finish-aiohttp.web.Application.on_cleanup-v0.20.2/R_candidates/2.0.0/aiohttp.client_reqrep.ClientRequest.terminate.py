    def terminate(self):
        if self._writer is not None:
            if not self.loop.is_closed():
                self._writer.cancel()
            self._writer = None
