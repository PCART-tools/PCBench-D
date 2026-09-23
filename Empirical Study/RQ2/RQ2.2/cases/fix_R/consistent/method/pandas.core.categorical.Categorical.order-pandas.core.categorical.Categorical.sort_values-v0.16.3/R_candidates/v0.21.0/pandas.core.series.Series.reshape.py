    def reshape(self, *args, **kwargs):
        """
        .. deprecated:: 0.19.0
           Calling this method will raise an error. Please call
           ``.values.reshape(...)`` instead.

        return an ndarray with the values shape
        if the specified shape matches exactly the current shape, then
        return self (for compat)

        See also
        --------
        numpy.ndarray.reshape
        """
        warnings.warn("reshape is deprecated and will raise "
                      "in a subsequent release. Please use "
                      ".values.reshape(...) instead", FutureWarning,
                      stacklevel=2)

        if len(args) == 1 and hasattr(args[0], '__iter__'):
            shape = args[0]
        else:
            shape = args

        if tuple(shape) == self.shape:
            # XXX ignoring the "order" keyword.
            nv.validate_reshape(tuple(), kwargs)
            return self

        return self._values.reshape(shape, **kwargs)
