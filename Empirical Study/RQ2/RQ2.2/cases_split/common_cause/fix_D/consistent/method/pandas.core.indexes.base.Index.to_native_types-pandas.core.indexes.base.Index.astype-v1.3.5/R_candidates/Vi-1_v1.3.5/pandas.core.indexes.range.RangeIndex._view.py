    def _view(self: RangeIndex) -> RangeIndex:
        result = type(self)._simple_new(self._range, name=self._name)
        result._cache = self._cache
        return result
