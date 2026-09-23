    @doc(Index._shallow_copy)
    def _shallow_copy(self, values=None, name=lib.no_default):
        names = name if name is not lib.no_default else self.names

        if values is not None:
            return type(self).from_tuples(values, sortorder=None, names=names)

        result = type(self)(
            levels=self.levels,
            codes=self.codes,
            sortorder=None,
            names=names,
            verify_integrity=False,
        )
        result._cache = self._cache.copy()
        result._cache.pop("levels", None)  # GH32669
        return result
