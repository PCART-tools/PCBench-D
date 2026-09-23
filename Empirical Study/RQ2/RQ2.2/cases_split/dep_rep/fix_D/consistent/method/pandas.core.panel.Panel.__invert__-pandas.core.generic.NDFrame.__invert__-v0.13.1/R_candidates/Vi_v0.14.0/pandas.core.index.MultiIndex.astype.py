    def astype(self, dtype):
        if np.dtype(dtype) != np.object_:
            raise TypeError('Setting %s dtype to anything other than object '
                            'is not supported' % self.__class__)
        return self._shallow_copy()
