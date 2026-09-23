    def to_sparse(self, kind='block', fill_value=None):
        """
        Convert Series to SparseSeries.

        Parameters
        ----------
        kind : {'block', 'integer'}
        fill_value : float, defaults to NaN (missing)

        Returns
        -------
        sp : SparseSeries
        """
        # TODO: deprecate
        from pandas.core.sparse.series import SparseSeries

        values = SparseArray(self, kind=kind, fill_value=fill_value)
        return SparseSeries(
            values, index=self.index, name=self.name
        ).__finalize__(self)
