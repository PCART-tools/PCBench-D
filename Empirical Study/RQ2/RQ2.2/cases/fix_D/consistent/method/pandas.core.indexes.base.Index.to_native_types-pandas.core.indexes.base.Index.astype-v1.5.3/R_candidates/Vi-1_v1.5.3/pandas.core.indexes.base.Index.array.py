    @cache_readonly  # type: ignore[misc]
    @doc(IndexOpsMixin.array)
    def array(self) -> ExtensionArray:
        array = self._data
        if isinstance(array, np.ndarray):
            from pandas.core.arrays.numpy_ import PandasArray

            array = PandasArray(array)
        return array
