    def _reduce(
        self, op, name, axis=0, skipna=True, numeric_only=None, filter_type=None, **kwds
    ):
        """ perform a reduction operation """
        return op(self.array.to_dense(), skipna=skipna, **kwds)
