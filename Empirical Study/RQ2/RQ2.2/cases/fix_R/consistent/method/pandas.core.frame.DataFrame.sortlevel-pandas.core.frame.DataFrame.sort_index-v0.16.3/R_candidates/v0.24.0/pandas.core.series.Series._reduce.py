    def _reduce(self, op, name, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        """
        Perform a reduction operation.

        If we have an ndarray as a value, then simply perform the operation,
        otherwise delegate to the object.
        """
        delegate = self._values

        if axis is not None:
            self._get_axis_number(axis)

        # dispatch to ExtensionArray interface
        if isinstance(delegate, ExtensionArray):
            return delegate._reduce(name, skipna=skipna, **kwds)
        elif is_datetime64_dtype(delegate):
            # use DatetimeIndex implementation to handle skipna correctly
            delegate = DatetimeIndex(delegate)

        # dispatch to numpy arrays
        elif isinstance(delegate, np.ndarray):
            if numeric_only:
                raise NotImplementedError('Series.{0} does not implement '
                                          'numeric_only.'.format(name))
            with np.errstate(all='ignore'):
                return op(delegate, skipna=skipna, **kwds)

        # TODO(EA) dispatch to Index
        # remove once all internals extension types are
        # moved to ExtensionArrays
        return delegate._reduce(op=op, name=name, axis=axis, skipna=skipna,
                                numeric_only=numeric_only,
                                filter_type=filter_type, **kwds)
