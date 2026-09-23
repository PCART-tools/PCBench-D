    @cache_readonly
    @Appender(IndexOpsMixin.array.__doc__)  # type: ignore
    def array(self) -> ExtensionArray:
        array = self._data
        if isinstance(array, np.ndarray):
            from pandas.core.arrays.numpy_ import PandasArray

            array = PandasArray(array)
        return array
