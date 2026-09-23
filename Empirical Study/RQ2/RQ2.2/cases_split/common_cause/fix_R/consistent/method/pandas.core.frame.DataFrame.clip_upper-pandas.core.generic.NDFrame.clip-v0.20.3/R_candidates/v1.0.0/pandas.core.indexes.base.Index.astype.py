    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        if is_dtype_equal(self.dtype, dtype):
            return self.copy() if copy else self

        elif is_categorical_dtype(dtype):
            from pandas.core.indexes.category import CategoricalIndex

            return CategoricalIndex(self.values, name=self.name, dtype=dtype, copy=copy)

        elif is_extension_array_dtype(dtype):
            return Index(np.asarray(self), dtype=dtype, copy=copy)

        try:
            casted = self.values.astype(dtype, copy=copy)
        except (TypeError, ValueError):
            raise TypeError(f"Cannot cast {type(self).__name__} to dtype {dtype}")
        return Index(casted, name=self.name, dtype=dtype)
