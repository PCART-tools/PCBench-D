    def delete(self, loc) -> None:
        """
        Delete given loc(-s) from block in-place.
        """
        # This will be unnecessary if/when __array_function__ is implemented
        self.values = self.values.delete(loc)
        self.mgr_locs = self._mgr_locs.delete(loc)
        try:
            self._cache.clear()
        except AttributeError:
            # _cache not yet initialized
            pass
