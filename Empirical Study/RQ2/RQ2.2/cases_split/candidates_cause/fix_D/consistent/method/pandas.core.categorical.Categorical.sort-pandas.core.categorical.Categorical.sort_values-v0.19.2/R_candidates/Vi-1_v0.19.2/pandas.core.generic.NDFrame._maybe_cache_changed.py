    def _maybe_cache_changed(self, item, value):
        """The object has called back to us saying maybe it has changed.

        numpy < 1.8 has an issue with object arrays and aliasing
        GH6026
        """
        self._data.set(item, value, check=pd._np_version_under1p8)
