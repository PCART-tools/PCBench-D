    def _reduce(self, op, axis=0, skipna=True, numeric_only=None,
                filter_type=None, name=None, **kwds):
        """
        perform a reduction operation

        if we have an ndarray as a value, then simply perform the operation,
        otherwise delegate to the object

        """
        delegate = self.values
        if isinstance(delegate, np.ndarray):
            return op(delegate, skipna=skipna, **kwds)

        return delegate._reduce(op=op, axis=axis, skipna=skipna, numeric_only=numeric_only,
                                filter_type=filter_type, name=name, **kwds)
