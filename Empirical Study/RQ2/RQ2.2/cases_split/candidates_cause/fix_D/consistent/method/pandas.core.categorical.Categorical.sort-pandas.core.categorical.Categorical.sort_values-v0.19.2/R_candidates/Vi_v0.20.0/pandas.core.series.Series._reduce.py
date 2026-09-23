    def _reduce(self, op, name, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        """
        perform a reduction operation

        if we have an ndarray as a value, then simply perform the operation,
        otherwise delegate to the object

        """
        delegate = self._values
        if isinstance(delegate, np.ndarray):
            # Validate that 'axis' is consistent with Series's single axis.
            self._get_axis_number(axis)
            if numeric_only:
                raise NotImplementedError('Series.{0} does not implement '
                                          'numeric_only.'.format(name))
            with np.errstate(all='ignore'):
                return op(delegate, skipna=skipna, **kwds)

        return delegate._reduce(op=op, name=name, axis=axis, skipna=skipna,
                                numeric_only=numeric_only,
                                filter_type=filter_type, **kwds)
