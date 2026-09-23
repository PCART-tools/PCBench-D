    def copy(self):
        """
        Copy array.  This is a no-op for dask.arrays, which are immutable
        """
        return Array(self.dask, self.name, self.chunks, self.dtype)
