    def __del__(self):
        if hasattr(self, '_tmpdir') and self._tmpdir:
            self._tmpdir.cleanup()
