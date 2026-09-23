    @classmethod
    def _from_sequence(
        cls, scalars, *, dtype: Dtype | None = None, copy: bool = False
    ) -> IntegerArray:
        values, mask = coerce_to_array(scalars, dtype=dtype, copy=copy)
        return IntegerArray(values, mask)
