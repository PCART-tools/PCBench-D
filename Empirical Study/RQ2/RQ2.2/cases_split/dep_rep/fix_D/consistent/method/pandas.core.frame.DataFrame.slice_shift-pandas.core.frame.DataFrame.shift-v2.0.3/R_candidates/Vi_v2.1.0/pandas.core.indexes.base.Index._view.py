    def _view(self) -> Self:
        """
        fastpath to make a shallow copy, i.e. new object with same data.
        """
        result = self._simple_new(self._values, name=self._name, refs=self._references)

        result._cache = self._cache
        return result
