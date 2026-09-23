    def _cleanup(self):  # Inline to finish() once cleanup() is removed.
        super()._cleanup()
        if self._tmpdir:
            _log.debug('MovieWriter: clearing temporary path=%s', self._tmpdir)
            self._tmpdir.cleanup()
        else:
            if self._clear_temp:
                _log.debug('MovieWriter: clearing temporary paths=%s',
                           self._temp_paths)
                for path in self._temp_paths:
                    path.unlink()
