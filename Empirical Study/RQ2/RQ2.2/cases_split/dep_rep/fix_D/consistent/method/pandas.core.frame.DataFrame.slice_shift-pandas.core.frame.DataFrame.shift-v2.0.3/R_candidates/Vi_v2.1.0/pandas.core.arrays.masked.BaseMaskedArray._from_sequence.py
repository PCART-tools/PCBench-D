    @classmethod
    def _from_sequence(cls, scalars, *, dtype=None, copy: bool = False) -> Self:
        values, mask = cls._coerce_to_array(scalars, dtype=dtype, copy=copy)
        return cls(values, mask)
