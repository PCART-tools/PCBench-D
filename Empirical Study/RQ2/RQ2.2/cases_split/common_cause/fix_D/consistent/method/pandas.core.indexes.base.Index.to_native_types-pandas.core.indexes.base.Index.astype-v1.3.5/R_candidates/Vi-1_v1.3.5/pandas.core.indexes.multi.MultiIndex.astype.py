    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)
        if is_categorical_dtype(dtype):
            msg = "> 1 ndim Categorical are not supported at this time"
            raise NotImplementedError(msg)
        elif not is_object_dtype(dtype):
            raise TypeError(
                "Setting a MultiIndex dtype to anything other than object "
                "is not supported"
            )
        elif copy is True:
            return self._view()
        return self
