    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        if isinstance(dtype, PandasDtype):
            dtype = dtype._dtype

        result = np.asarray(scalars, dtype=dtype)
        if copy and result is scalars:
            result = result.copy()
        return cls(result)
