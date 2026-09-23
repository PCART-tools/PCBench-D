    @classmethod
    def _make_accessor(cls, data):
        if not is_categorical_dtype(data.dtype):
            raise AttributeError("Can only use .cat accessor with a "
                                 "'category' dtype")
        return CategoricalAccessor(data.values, data.index,
                                   getattr(data, 'name', None),)
