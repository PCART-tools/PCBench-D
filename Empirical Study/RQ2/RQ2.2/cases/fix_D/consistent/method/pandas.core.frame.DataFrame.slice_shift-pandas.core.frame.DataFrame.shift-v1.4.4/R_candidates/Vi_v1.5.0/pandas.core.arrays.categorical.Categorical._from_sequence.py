    @classmethod
    def _from_sequence(cls, scalars, *, dtype: Dtype | None = None, copy=False):
        return Categorical(scalars, dtype=dtype, copy=copy)
