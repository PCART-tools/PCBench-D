    def to_imperative(self):
        """ Convert bag to dask Values

        Returns list of values, one value per partition.
        """
        from dask.imperative import Value
        return [Value(k, [self.dask]) for k in self._keys()]
