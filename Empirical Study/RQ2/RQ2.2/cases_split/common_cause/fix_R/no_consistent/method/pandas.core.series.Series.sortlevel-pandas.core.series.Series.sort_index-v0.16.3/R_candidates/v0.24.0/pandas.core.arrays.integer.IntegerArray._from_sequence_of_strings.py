    @classmethod
    def _from_sequence_of_strings(cls, strings, dtype=None, copy=False):
        scalars = to_numeric(strings, errors="raise")
        return cls._from_sequence(scalars, dtype, copy)
