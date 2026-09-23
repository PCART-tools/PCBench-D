    def _consolidate_inplace(self):
        new_values = np.concatenate([c.sp_values for c in self._chunks])
        new_index = _concat_sparse_indexes([c.sp_index for c in self._chunks])
        new_arr = SparseArray(new_values, sparse_index=new_index,
                              fill_value=self.fill_value)
        self._chunks = [new_arr]
