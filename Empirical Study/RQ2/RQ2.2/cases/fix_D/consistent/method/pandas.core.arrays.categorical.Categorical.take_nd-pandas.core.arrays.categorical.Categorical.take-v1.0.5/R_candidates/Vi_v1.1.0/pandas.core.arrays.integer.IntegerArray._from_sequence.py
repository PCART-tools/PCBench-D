    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy: bool = False) -> "IntegerArray":
        return integer_array(scalars, dtype=dtype, copy=copy)
