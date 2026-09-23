    @Appender(generic._shared_docs['isnotnull'])
    def isnotnull(self):
        arr = SparseArray(notnull(self.values.sp_values),
                          sparse_index=self.values.sp_index,
                          fill_value=notnull(self.fill_value))
        return self._constructor(arr, index=self.index).__finalize__(self)
