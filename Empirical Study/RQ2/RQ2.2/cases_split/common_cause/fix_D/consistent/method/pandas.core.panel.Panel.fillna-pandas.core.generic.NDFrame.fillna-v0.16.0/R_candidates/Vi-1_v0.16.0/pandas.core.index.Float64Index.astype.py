    def astype(self, dtype):
        if np.dtype(dtype) not in (np.object, np.float64):
            raise TypeError('Setting %s dtype to anything other than '
                            'float64 or object is not supported' %
                            self.__class__)
        return Index(self.values, name=self.name, dtype=dtype)
