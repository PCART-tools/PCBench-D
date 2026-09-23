    def set_value(self, index, col, value, takeable=False):
        """
        Put single value at passed column and index

        Parameters
        ----------
        index : row label
        col : column label
        value : scalar value
        takeable : interpret the index/col as indexers, default False

        Notes
        -----
        This method *always* returns a new object. It is currently not
        particularly efficient (and potentially very expensive) but is provided
        for API compatibility with DataFrame

        Returns
        -------
        frame : DataFrame
        """
        dense = self.to_dense().set_value(index, col, value, takeable=takeable)
        return dense.to_sparse(kind=self._default_kind,
                               fill_value=self._default_fill_value)
