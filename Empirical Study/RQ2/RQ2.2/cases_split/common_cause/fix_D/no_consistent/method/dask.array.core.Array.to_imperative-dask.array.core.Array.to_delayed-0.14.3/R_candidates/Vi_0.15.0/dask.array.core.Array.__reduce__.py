    def __reduce__(self):
        return (Array, (self.dask, self.name, self.chunks, self.dtype))
