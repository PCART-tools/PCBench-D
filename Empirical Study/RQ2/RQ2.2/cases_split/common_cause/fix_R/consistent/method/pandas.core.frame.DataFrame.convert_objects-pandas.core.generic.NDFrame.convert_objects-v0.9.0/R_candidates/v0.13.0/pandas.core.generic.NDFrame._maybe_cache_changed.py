    def _maybe_cache_changed(self, item, value):
        """ the object has called back to us saying
        maybe it has changed """
        self._data.set(item, value)
