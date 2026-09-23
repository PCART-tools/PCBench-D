    @cache_readonly
    def cat(self):
        from pandas.core.categorical import CategoricalAccessor
        if not com.is_categorical_dtype(self.dtype):
            raise TypeError("Can only use .cat accessor with a 'category' dtype")
        return CategoricalAccessor(self.values, self.index)
