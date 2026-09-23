    @staticmethod
    def _validate(data):
        if not isinstance(data.dtype, CategoricalDtype):
            raise AttributeError("Can only use .cat accessor with a 'category' dtype")
