    @Appender(generic._shared_docs['notna'])
    def notna(self):
        arr = SparseArray(notna(self.values.sp_values),
                          sparse_index=self.values.sp_index,
                          fill_value=notna(self.fill_value))
        return self._constructor(arr, index=self.index).__finalize__(self)
