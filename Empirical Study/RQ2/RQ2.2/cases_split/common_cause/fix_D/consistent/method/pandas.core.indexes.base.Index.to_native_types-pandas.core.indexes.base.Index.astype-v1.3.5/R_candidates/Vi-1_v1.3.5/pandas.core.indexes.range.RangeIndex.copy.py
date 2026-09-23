    @doc(Int64Index.copy)
    def copy(
        self,
        name: Hashable = None,
        deep: bool = False,
        dtype: Dtype | None = None,
        names=None,
    ):
        name = self._validate_names(name=name, names=names, deep=deep)[0]
        new_index = self._rename(name=name)

        if dtype:
            warnings.warn(
                "parameter dtype is deprecated and will be removed in a future "
                "version. Use the astype method instead.",
                FutureWarning,
                stacklevel=2,
            )
            new_index = new_index.astype(dtype)
        return new_index
