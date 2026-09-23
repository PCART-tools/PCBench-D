    def __new__(
        cls,
        data=None,
        categories=None,
        ordered=None,
        dtype: Dtype | None = None,
        copy: bool = False,
        name: Hashable = None,
    ) -> CategoricalIndex:

        name = maybe_extract_name(name, data, cls)

        if data is None:
            # GH#38944
            warnings.warn(
                "Constructing a CategoricalIndex without passing data is "
                "deprecated and will raise in a future version. "
                "Use CategoricalIndex([], ...) instead",
                FutureWarning,
                stacklevel=2,
            )
            data = []

        if is_scalar(data):
            raise cls._scalar_data_error(data)

        data = Categorical(
            data, categories=categories, ordered=ordered, dtype=dtype, copy=copy
        )

        return cls._simple_new(data, name=name)
