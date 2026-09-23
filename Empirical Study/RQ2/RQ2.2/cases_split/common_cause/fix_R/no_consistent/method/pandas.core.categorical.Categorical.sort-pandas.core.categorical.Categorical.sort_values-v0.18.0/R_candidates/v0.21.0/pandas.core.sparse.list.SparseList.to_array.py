    def to_array(self):
        """
        Return SparseArray from data stored in the SparseList

        Returns
        -------
        sparr : SparseArray
        """
        self.consolidate(inplace=True)
        return self._chunks[0]
