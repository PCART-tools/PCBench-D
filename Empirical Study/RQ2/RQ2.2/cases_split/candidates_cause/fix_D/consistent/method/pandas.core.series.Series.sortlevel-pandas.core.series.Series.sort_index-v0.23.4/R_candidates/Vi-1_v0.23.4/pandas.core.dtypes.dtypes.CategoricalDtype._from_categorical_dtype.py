    @classmethod
    def _from_categorical_dtype(cls, dtype, categories=None, ordered=None):
        if categories is ordered is None:
            return dtype
        if categories is None:
            categories = dtype.categories
        if ordered is None:
            ordered = dtype.ordered
        return cls(categories, ordered)
