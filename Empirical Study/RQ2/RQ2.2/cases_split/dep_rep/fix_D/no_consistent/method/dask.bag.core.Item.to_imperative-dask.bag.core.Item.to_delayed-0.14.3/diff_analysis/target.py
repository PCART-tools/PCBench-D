    def to_imperative(self):
        """ Convert bag item to dask Value

        Returns a single value.
        """
        from dask.imperative import Value
        return Value(self.key, [self.dask])
