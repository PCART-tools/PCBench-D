    def copy(self, deep=True):
        """
        Make a copy of the SparseSeries. Only the actual sparse values need to
        be copied
        """
        new_data = self._data
        if deep:
            new_data = self._data.copy()

        return self._constructor(new_data, sparse_index=self.sp_index,
                                 fill_value=self.fill_value).__finalize__(self)
