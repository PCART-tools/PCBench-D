    @classmethod
    def _from_factorized(cls, values, original):
        assert values.dtype == original._ndarray.dtype
        return original._from_backing_data(values)
