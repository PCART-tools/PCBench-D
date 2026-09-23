    @classmethod
    def _from_sequence_of_strings(
        cls, strings, dtype=None, copy=False
    ) -> "PeriodArray":
        return cls._from_sequence(strings, dtype, copy)
