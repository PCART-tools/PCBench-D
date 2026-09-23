    @cache_readonly
    @doc(IndexOpsMixin.array)
    def array(self) -> ExtensionArray:
        array = self._data
        if isinstance(array, np.ndarray):
            from pandas.core.arrays.numpy_ import NumpyExtensionArray

            array = NumpyExtensionArray(array)
        return array
