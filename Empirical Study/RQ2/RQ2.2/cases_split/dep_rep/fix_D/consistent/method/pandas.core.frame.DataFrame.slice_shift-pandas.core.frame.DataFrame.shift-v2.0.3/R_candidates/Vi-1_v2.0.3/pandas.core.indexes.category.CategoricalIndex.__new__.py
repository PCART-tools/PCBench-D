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

        if is_scalar(data):
            # GH#38944 include None here, which pre-2.0 subbed in []
            cls._raise_scalar_data_error(data)

        data = Categorical(
            data, categories=categories, ordered=ordered, dtype=dtype, copy=copy
        )

        return cls._simple_new(data, name=name)
