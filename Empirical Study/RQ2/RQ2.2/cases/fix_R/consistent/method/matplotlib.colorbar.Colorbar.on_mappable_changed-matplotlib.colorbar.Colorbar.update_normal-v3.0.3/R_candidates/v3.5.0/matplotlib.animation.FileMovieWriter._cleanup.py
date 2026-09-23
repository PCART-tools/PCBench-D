    def _cleanup(self):  # Inline to finish() once cleanup() is removed.
        super()._cleanup()
        if self._tmpdir:
            _log.debug('MovieWriter: clearing temporary path=%s', self._tmpdir)
            self._tmpdir.cleanup()
