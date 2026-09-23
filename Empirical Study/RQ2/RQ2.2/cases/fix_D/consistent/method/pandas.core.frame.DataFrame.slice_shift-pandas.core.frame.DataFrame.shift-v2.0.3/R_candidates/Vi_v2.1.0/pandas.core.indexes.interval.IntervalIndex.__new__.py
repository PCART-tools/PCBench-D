    def __new__(
        cls,
        data,
        closed: IntervalClosedType | None = None,
        dtype: Dtype | None = None,
        copy: bool = False,
        name: Hashable | None = None,
        verify_integrity: bool = True,
    ) -> IntervalIndex:
        name = maybe_extract_name(name, data, cls)

        with rewrite_exception("IntervalArray", cls.__name__):
            array = IntervalArray(
                data,
                closed=closed,
                copy=copy,
                dtype=dtype,
                verify_integrity=verify_integrity,
            )

        return cls._simple_new(array, name)
