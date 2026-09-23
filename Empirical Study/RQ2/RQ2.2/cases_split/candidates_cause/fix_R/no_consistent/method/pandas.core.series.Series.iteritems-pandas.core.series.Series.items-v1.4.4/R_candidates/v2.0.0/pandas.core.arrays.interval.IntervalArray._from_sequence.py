    @classmethod
    def _from_sequence(
        cls: type[IntervalArrayT],
        scalars,
        *,
        dtype: Dtype | None = None,
        copy: bool = False,
    ) -> IntervalArrayT:
        return cls(scalars, dtype=dtype, copy=copy)
