    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_categorical_dtype(dtype):
            msg = "> 1 ndim Categorical are not supported at this time"
            raise NotImplementedError(msg)
        elif not is_object_dtype(dtype):
            msg = (
                "Setting {cls} dtype to anything other than object " "is not supported"
            ).format(cls=self.__class__)
            raise TypeError(msg)
        elif copy is True:
            return self._shallow_copy()
        return self
