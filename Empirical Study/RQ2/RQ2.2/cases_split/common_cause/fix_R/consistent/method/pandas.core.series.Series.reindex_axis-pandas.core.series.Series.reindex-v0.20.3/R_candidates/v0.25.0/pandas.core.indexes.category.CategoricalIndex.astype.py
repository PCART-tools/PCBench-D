    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        if is_interval_dtype(dtype):
            from pandas import IntervalIndex

            return IntervalIndex(np.array(self))
        elif is_categorical_dtype(dtype):
            # GH 18630
            dtype = self.dtype.update_dtype(dtype)
            if dtype == self.dtype:
                return self.copy() if copy else self

        return super().astype(dtype=dtype, copy=copy)
