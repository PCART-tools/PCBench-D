    def to_dense(self, sparse_only=False):
        """
        Convert SparseSeries to a Series.

        Parameters
        ----------
        sparse_only : bool, default False
            .. deprecated:: 0.20.0
                This argument will be removed in a future version.

            If True, return just the non-sparse values, or the dense version
            of `self.values` if False.

        Returns
        -------
        s : Series
        """
        if sparse_only:
            warnings.warn(("The 'sparse_only' parameter has been deprecated "
                           "and will be removed in a future version."),
                          FutureWarning, stacklevel=2)
            int_index = self.sp_index.to_int_index()
            index = self.index.take(int_index.indices)
            return Series(self.sp_values, index=index, name=self.name)
        else:
            return Series(self.values.to_dense(), index=self.index,
                          name=self.name)
