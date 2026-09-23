    @classmethod
    def _from_factorized(cls, values, original: "BooleanArray"):
        return cls._from_sequence(values, dtype=original.dtype)
