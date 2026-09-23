    def to_sparse(self, kind="block", fill_value=None):
        """
        Convert Series to SparseSeries.

        .. deprecated:: 0.25.0

        Parameters
        ----------
        kind : {'block', 'integer'}, default 'block'
        fill_value : float, defaults to NaN (missing)
            Value to use for filling NaN values.

        Returns
        -------
        SparseSeries
            Sparse representation of the Series.
        """

        warnings.warn(
            "Series.to_sparse is deprecated and will be removed " "in a future version",
            FutureWarning,
            stacklevel=2,
        )
        from pandas.core.sparse.series import SparseSeries

        values = SparseArray(self, kind=kind, fill_value=fill_value)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="SparseSeries")
            return SparseSeries(values, index=self.index, name=self.name).__finalize__(
                self
            )
