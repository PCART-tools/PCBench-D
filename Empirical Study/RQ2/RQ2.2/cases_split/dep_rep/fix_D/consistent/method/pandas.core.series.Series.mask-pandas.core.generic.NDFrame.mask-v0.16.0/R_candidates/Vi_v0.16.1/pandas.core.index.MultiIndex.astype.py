    def astype(self, dtype):
        if not is_object_dtype(np.dtype(dtype)):
            raise TypeError('Setting %s dtype to anything other than object '
                            'is not supported' % self.__class__)
        return self._shallow_copy()
