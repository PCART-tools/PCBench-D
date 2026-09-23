    @doc(Int64Index.copy)
    def copy(self, name=None, deep=False, dtype=None, names=None):
        name = self._validate_names(name=name, names=names, deep=deep)[0]
        new_index = self._shallow_copy(name=name)

        if dtype:
            warnings.warn(
                "parameter dtype is deprecated and will be removed in a future "
                "version. Use the astype method instead.",
                FutureWarning,
                stacklevel=2,
            )
            new_index = new_index.astype(dtype)
        return new_index
