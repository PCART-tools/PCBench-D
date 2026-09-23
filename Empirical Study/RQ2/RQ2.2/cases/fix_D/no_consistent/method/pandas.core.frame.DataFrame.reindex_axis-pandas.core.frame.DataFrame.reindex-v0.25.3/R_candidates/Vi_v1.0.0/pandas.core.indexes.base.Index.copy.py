    @Appender(_index_shared_docs["copy"])
    def copy(self, name=None, deep=False, dtype=None, **kwargs):
        if deep:
            new_index = self._shallow_copy(self._data.copy())
        else:
            new_index = self._shallow_copy()

        names = kwargs.get("names")
        names = self._validate_names(name=name, names=names, deep=deep)
        new_index = new_index.set_names(names)

        if dtype:
            new_index = new_index.astype(dtype)
        return new_index
