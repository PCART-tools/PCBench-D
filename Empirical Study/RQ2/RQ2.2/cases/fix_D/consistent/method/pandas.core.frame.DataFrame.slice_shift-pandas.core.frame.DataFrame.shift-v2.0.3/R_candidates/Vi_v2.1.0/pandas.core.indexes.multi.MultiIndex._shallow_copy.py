    @doc(Index._shallow_copy)
    def _shallow_copy(self, values: np.ndarray, name=lib.no_default) -> MultiIndex:
        names = name if name is not lib.no_default else self.names

        return type(self).from_tuples(values, sortorder=None, names=names)
