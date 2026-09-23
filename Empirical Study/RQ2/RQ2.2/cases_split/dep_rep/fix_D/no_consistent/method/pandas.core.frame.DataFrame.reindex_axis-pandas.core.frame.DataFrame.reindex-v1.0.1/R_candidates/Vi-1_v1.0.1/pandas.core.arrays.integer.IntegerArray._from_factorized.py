    @classmethod
    def _from_factorized(cls, values, original):
        return integer_array(values, dtype=original.dtype)
