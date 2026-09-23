    def finish(self):
        # Call run here now that all frame grabbing is done. All temp files
        # are available to be assembled.
        try:
            self._run()
            super().finish()
        finally:
            if self._tmpdir:
                _log.debug(
                    'MovieWriter: clearing temporary path=%s', self._tmpdir
                )
                self._tmpdir.cleanup()
