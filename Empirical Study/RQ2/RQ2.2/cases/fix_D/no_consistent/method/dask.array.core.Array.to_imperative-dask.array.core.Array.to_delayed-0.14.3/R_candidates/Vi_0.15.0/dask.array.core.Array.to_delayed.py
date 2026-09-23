    def to_delayed(self):
        """ Convert Array into dask Delayed objects

        Returns an array of values, one value per chunk.

        See Also
        --------
        dask.array.from_delayed
        """
        from ..delayed import Delayed
        dsk = self._optimize(self.dask, self._keys())
        L = ndeepmap(self.ndim, lambda k: Delayed(k, dsk), self._keys())
        return np.array(L, dtype=object)
