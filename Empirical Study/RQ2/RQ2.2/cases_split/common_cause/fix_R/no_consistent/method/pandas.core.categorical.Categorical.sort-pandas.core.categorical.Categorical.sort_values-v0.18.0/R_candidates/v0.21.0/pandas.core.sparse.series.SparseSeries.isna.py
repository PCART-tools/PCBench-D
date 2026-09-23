    @Appender(generic._shared_docs['isna'])
    def isna(self):
        arr = SparseArray(isna(self.values.sp_values),
                          sparse_index=self.values.sp_index,
                          fill_value=isna(self.fill_value))
        return self._constructor(arr, index=self.index).__finalize__(self)
