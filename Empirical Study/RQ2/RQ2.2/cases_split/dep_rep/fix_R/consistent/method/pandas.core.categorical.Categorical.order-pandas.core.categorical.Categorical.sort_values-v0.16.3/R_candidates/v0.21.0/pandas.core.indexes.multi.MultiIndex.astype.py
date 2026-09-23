    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        if not is_object_dtype(np.dtype(dtype)):
            raise TypeError('Setting %s dtype to anything other than object '
                            'is not supported' % self.__class__)
        elif copy is True:
            return self._shallow_copy()
        return self
