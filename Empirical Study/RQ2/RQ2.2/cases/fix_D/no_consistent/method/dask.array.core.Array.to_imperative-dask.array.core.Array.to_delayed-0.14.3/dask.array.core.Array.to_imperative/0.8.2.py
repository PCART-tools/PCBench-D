    def to_imperative(self):
        """ Convert Array into dask Values

        Returns an array of values, one value per chunk.
        """
        from ..imperative import Value
        return np.array(deepmap(lambda k: Value(k, [self.dask]), self._keys()),
                        dtype=object)
