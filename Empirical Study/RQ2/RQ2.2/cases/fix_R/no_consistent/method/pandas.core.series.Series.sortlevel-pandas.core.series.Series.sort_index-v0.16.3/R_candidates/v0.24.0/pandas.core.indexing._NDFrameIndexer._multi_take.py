    def _multi_take(self, tup):
        """
        Create the indexers for the passed tuple of keys, and execute the take
        operation. This allows the take operation to be executed all at once -
        rather than once for each dimension - improving efficiency.

        Parameters
        ----------
        tup : tuple
            Tuple of indexers, one per axis

        Returns
        -------
        values: same type as the object being indexed
        """
        # GH 836
        o = self.obj
        d = {axis: self._get_listlike_indexer(key, axis)
             for (key, axis) in zip(tup, o._AXIS_ORDERS)}
        return o._reindex_with_indexers(d, copy=True, allow_dups=True)
