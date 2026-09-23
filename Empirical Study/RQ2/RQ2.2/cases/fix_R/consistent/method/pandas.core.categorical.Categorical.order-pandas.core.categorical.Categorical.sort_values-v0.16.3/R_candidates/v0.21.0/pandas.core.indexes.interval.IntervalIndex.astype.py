    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        if is_interval_dtype(dtype):
            if copy:
                self = self.copy()
            return self
        elif is_object_dtype(dtype):
            return Index(self.values, dtype=object)
        elif is_categorical_dtype(dtype):
            from pandas import Categorical
            return Categorical(self, ordered=True)
        raise ValueError('Cannot cast IntervalIndex to dtype %s' % dtype)
