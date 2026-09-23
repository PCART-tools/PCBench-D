    def _make_cat_accessor(self):
        if not com.is_categorical_dtype(self.dtype):
            raise AttributeError("Can only use .cat accessor with a "
                                 "'category' dtype")
        return CategoricalAccessor(self.values, self.index)
