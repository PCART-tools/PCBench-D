    def _reset_cacher(self) -> None:
        """Reset the cacher."""
        if hasattr(self, "_cacher"):
            del self._cacher
