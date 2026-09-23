    @property
    def _is_cached(self):
        """Return boolean indicating if self is cached or not."""
        return getattr(self, "_cacher", None) is not None
