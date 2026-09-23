    @classmethod
    def _from_sequence(
        cls, scalars, *, dtype: Dtype | None = None, copy: bool = False
    ) -> Categorical:
        return Categorical(scalars, dtype=dtype, copy=copy)
