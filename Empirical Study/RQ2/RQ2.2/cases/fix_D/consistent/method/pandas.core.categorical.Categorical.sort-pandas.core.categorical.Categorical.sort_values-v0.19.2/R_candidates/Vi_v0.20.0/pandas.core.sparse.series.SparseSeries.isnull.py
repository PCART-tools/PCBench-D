    @Appender(generic._shared_docs['isnull'])
    def isnull(self):
        arr = SparseArray(isnull(self.values.sp_values),
                          sparse_index=self.values.sp_index,
                          fill_value=isnull(self.fill_value))
        return self._constructor(arr, index=self.index).__finalize__(self)
