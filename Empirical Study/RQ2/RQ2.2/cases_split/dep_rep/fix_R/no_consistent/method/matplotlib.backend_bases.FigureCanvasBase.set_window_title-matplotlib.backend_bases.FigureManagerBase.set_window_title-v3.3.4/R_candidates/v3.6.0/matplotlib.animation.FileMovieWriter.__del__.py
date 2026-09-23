    def __del__(self):
        if self._tmpdir:
            self._tmpdir.cleanup()
