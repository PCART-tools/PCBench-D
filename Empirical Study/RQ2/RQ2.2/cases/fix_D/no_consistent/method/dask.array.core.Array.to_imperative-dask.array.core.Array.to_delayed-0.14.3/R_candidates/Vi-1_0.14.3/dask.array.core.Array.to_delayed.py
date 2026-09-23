    def to_delayed(self):
        """ Convert Array into dask Delayed objects

        Returns an array of values, one value per chunk.

        See Also
        --------
        dask.array.from_delayed
        """
        from ..delayed import Delayed
        return np.array(ndeepmap(self.ndim, lambda k: Delayed(k, self.dask), self._keys()),
                        dtype=object)
