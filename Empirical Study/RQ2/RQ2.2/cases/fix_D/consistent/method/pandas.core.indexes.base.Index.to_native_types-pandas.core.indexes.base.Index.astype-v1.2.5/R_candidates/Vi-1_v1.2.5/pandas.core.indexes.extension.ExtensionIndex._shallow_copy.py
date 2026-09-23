    @doc(Index._shallow_copy)
    def _shallow_copy(
        self, values: Optional[ExtensionArray] = None, name: Label = lib.no_default
    ):
        name = self.name if name is lib.no_default else name

        if values is not None:
            return self._simple_new(values, name=name)

        result = self._simple_new(self._data, name=name)
        result._cache = self._cache
        return result
