    def to_delayed(self):
        """ Convert bag to list of dask Delayed

        Returns list of Delayed, one per partition.
        """
        from dask.delayed import Delayed
        dsk = self._optimize(self.dask, self._keys())
        return [Delayed(k, dsk) for k in self._keys()]
