    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)
        if isinstance(dtype, CategoricalDtype):
            msg = "> 1 ndim Categorical are not supported at this time"
            raise NotImplementedError(msg)
        if not is_object_dtype(dtype):
            raise TypeError(
                "Setting a MultiIndex dtype to anything other than object "
                "is not supported"
            )
        if copy is True:
            return self._view()
        return self
