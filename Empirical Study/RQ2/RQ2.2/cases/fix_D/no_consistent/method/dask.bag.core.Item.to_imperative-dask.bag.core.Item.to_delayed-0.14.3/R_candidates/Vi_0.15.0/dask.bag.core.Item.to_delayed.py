    def to_delayed(self):
        """ Convert bag item to dask Delayed

        Returns a single value.
        """
        from dask.delayed import Delayed
        dsk = self._optimize(self.dask, [self.key])
        return Delayed(self.key, dsk)
