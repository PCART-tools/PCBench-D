    @classmethod
    def _from_sequence_of_strings(
        cls, strings, *, dtype: Dtype | None = None, copy: bool = False
    ) -> PeriodArray:
        return cls._from_sequence(strings, dtype=dtype, copy=copy)
