    @classmethod
    def _from_sequence_of_strings(
        cls: type[T], strings, *, dtype: Dtype | None = None, copy: bool = False
    ) -> T:
        from pandas.core.tools.numeric import to_numeric

        scalars = to_numeric(strings, errors="raise")
        return cls._from_sequence(scalars, dtype=dtype, copy=copy)
