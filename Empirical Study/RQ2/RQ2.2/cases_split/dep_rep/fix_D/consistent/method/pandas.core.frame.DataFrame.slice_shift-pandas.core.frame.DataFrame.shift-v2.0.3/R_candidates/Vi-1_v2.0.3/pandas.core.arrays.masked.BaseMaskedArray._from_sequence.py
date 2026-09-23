    @classmethod
    def _from_sequence(
        cls: type[BaseMaskedArrayT], scalars, *, dtype=None, copy: bool = False
    ) -> BaseMaskedArrayT:
        values, mask = cls._coerce_to_array(scalars, dtype=dtype, copy=copy)
        return cls(values, mask)
