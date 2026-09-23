    @classmethod
    def _from_sequence(
        cls, scalars, *, dtype: Dtype | None = None, copy: bool = False
    ) -> BooleanArray:
        if dtype:
            assert dtype == "boolean"
        values, mask = coerce_to_array(scalars, copy=copy)
        return BooleanArray(values, mask)
