    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        return Categorical(scalars, dtype=dtype)
