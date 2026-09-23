    @Appender(generic._shared_docs['shift'] % _shared_doc_kwargs)
    def shift(self, periods, freq=None, axis=0):
        if periods == 0:
            return self.copy()

        # no special handling of fill values yet
        if not isna(self.fill_value):
            shifted = self.to_dense().shift(periods, freq=freq,
                                            axis=axis)
            return shifted.to_sparse(fill_value=self.fill_value,
                                     kind=self.kind)

        if freq is not None:
            return self._constructor(
                self.sp_values, sparse_index=self.sp_index,
                index=self.index.shift(periods, freq),
                fill_value=self.fill_value).__finalize__(self)

        int_index = self.sp_index.to_int_index()
        new_indices = int_index.indices + periods
        start, end = new_indices.searchsorted([0, int_index.length])

        new_indices = new_indices[start:end]
        new_sp_index = _make_index(len(self), new_indices, self.sp_index)

        arr = self.values._simple_new(self.sp_values[start:end].copy(),
                                      new_sp_index, fill_value=np.nan)
        return self._constructor(arr, index=self.index).__finalize__(self)
