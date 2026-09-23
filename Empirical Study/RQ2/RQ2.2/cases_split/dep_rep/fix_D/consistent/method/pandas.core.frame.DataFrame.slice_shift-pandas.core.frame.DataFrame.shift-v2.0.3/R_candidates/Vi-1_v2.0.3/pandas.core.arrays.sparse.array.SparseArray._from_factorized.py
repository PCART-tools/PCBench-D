    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values, dtype=original.dtype)
