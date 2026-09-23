    @classmethod
    def _from_sequence_of_strings(
        cls, strings, *, dtype: Dtype | None = None, copy: bool = False
    ) -> Self:
        from pandas.core.tools.numeric import to_numeric

        scalars = to_numeric(strings, errors="raise", dtype_backend="numpy_nullable")
        return cls._from_sequence(scalars, dtype=dtype, copy=copy)
