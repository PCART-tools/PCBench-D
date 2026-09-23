    @classmethod
    def _from_sequence(
        cls, scalars, *, dtype=None, copy: bool = False
    ) -> FloatingArray:
        values, mask = coerce_to_array(scalars, dtype=dtype, copy=copy)
        return FloatingArray(values, mask)
