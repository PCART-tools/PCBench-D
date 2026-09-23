    def _view(self) -> MultiIndex:
        result = type(self)(
            levels=self.levels,
            codes=self.codes,
            sortorder=self.sortorder,
            names=self.names,
            verify_integrity=False,
        )
        result._cache = self._cache.copy()
        result._cache.pop("levels", None)  # GH32669
        return result
