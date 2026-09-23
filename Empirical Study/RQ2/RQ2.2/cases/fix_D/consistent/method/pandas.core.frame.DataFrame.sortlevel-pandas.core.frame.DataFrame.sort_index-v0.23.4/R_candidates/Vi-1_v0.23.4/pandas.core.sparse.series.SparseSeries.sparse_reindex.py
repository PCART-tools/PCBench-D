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
            raise TypeError('new index must be a SparseIndex')

        block = self.block.sparse_reindex(new_index)
        new_data = SingleBlockManager(block, self.index)
        return self._constructor(new_data, index=self.index,
                                 sparse_index=new_index,
                                 fill_value=self.fill_value).__finalize__(self)
