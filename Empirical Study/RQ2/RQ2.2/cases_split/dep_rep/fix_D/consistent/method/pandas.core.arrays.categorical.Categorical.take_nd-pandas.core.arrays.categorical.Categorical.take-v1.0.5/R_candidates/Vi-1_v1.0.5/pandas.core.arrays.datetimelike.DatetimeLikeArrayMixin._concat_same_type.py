    @classmethod
    def _concat_same_type(cls, to_concat):
        dtypes = {x.dtype for x in to_concat}
        assert len(dtypes) == 1
        dtype = list(dtypes)[0]

        values = np.concatenate([x.asi8 for x in to_concat])
        return cls(values, dtype=dtype)
