    @property
    def _int64index(self) -> Int64Index:
        # wrap _cached_int64index so we can be sure its name matches self.name
        res = self._cached_int64index
        res._name = self._name
        return res
