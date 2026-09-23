    def __setitem__(self, key, value):
        if isinstance(key, Array):
            if isinstance(value, Array) and value.ndim > 1:
                raise ValueError('boolean index array should have 1 dimension')
            y = where(key, value, self)
            self.dtype = y.dtype
            self.dask = y.dask
            self.name = y.name
            return self
        else:
            raise NotImplementedError("Item assignment with %s not supported"
                                      % type(key))
