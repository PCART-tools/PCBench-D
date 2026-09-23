    def set_value(self, label, value, takeable=False):
        """
        Quickly set single value at passed label. If label is not contained, a
        new object is created with the label placed at the end of the result
        index

        Parameters
        ----------
        label : object
            Partial indexing with MultiIndex not allowed
        value : object
            Scalar value
        takeable : interpret the index as indexers, default False

        Notes
        -----
        This method *always* returns a new object. It is not particularly
        efficient but is provided for API compatibility with Series

        Returns
        -------
        series : SparseSeries
        """
        values = self.to_dense()

        # if the label doesn't exist, we will create a new object here
        # and possibily change the index
        new_values = values.set_value(label, value, takeable=takeable)
        if new_values is not None:
            values = new_values
        new_index = values.index
        values = SparseArray(values, fill_value=self.fill_value,
                             kind=self.kind)
        self._data = SingleBlockManager(values, new_index)
        self._index = new_index
