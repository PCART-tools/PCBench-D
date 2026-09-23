    @classmethod
    def _from_categorical_dtype(
        cls, dtype: "CategoricalDtype", categories=None, ordered: OrderedType = None
    ) -> "CategoricalDtype":
        if categories is ordered is None:
            return dtype
        if categories is None:
            categories = dtype.categories
        if ordered is None:
            ordered = dtype.ordered
        return cls(categories, ordered)
