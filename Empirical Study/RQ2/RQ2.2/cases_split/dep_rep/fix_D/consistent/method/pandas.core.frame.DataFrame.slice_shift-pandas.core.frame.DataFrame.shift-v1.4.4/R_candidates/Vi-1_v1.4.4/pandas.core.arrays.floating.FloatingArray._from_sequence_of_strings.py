    @classmethod
    def _from_sequence_of_strings(
        cls, strings, *, dtype=None, copy: bool = False
    ) -> FloatingArray:
        scalars = to_numeric(strings, errors="raise")
        return cls._from_sequence(scalars, dtype=dtype, copy=copy)
