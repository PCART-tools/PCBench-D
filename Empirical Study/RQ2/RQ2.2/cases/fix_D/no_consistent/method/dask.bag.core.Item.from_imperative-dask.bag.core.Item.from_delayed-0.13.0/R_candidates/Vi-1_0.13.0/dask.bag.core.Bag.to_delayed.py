    def to_delayed(self):
        """ Convert bag to list of dask Delayed

        Returns list of Delayed, one per partition.
        """
        from dask.delayed import Delayed
        return [Delayed(k, [self.dask]) for k in self._keys()]
