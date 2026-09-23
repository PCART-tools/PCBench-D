    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        if is_interval_dtype(dtype):
            from pandas import IntervalIndex
            return IntervalIndex.from_intervals(np.array(self))
        return super(CategoricalIndex, self).astype(dtype=dtype, copy=copy)
