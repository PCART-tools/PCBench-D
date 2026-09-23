    def __repr__(self):
        """

        >>> import dask.array as da
        >>> da.ones((10, 10), chunks=(5, 5), dtype='i4')
        dask.array<..., shape=(10, 10), dtype=int32, chunksize=(5, 5)>
        """
        chunksize = str(tuple(c[0] if c else 0 for c in self.chunks))
        name = self.name.rsplit('-', 1)[0]
        return ("dask.array<%s, shape=%s, dtype=%s, chunksize=%s>" %
                (name, self.shape, self.dtype, chunksize))
