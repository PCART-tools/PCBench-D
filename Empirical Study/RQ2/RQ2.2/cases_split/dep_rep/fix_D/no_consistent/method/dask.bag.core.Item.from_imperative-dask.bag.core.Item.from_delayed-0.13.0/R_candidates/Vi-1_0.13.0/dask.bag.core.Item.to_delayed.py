    def to_delayed(self):
        """ Convert bag item to dask Delayed

        Returns a single value.
        """
        from dask.delayed import Delayed
        return Delayed(self.key, [self.dask])
