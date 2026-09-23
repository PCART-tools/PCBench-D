    def _reset_cacher(self) -> None:
        """
        Reset the cacher.
        """
        if hasattr(self, "_cacher"):
            # should only get here with self.ndim == 1
            del self._cacher
