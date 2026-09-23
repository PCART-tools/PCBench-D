    def copy(self, deep=True):
        """
        Make a copy of the SparseArray. Only the actual sparse values need to
        be copied.
        """
        if deep:
            values = self.sp_values.copy()
        else:
            values = self.sp_values
        return SparseArray(values, sparse_index=self.sp_index,
                           dtype=self.dtype, fill_value=self.fill_value)
