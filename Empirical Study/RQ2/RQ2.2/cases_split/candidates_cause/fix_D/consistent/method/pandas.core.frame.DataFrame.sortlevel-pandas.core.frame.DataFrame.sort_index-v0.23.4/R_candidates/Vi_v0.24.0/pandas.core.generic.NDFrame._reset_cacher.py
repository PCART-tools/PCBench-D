    def _reset_cacher(self):
        """Reset the cacher."""
        if hasattr(self, '_cacher'):
            del self._cacher
