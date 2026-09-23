    def sparse_reindex(self, new_index):
        """
        Conform sparse values to new SparseIndex

        Parameters
        ----------
        new_index : {BlockIndex, IntIndex}

        Returns
        -------
        reindexed : SparseSeries
        """
        if not isinstance(new_index, splib.SparseIndex):
            raise TypeError("new index must be a SparseIndex")
        values = self.values
        values = values.sp_index.to_int_index().reindex(
            values.sp_values.astype("float64"), values.fill_value, new_index
        )
        values = SparseArray(
            values, sparse_index=new_index, fill_value=self.values.fill_value
        )
        return self._constructor(values, index=self.index).__finalize__(self)
