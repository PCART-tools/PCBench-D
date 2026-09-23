    def reshape(self, *args, **kwargs):
        """
        return an ndarray with the values shape
        if the specified shape matches exactly the current shape, then
        return self (for compat)

        See also
        --------
        numpy.ndarray.take
        """
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            shape = args[0]
        else:
            shape = args

        if tuple(shape) == self.shape:
            # XXX ignoring the "order" keyword.
            return self

        return self.values.reshape(shape, **kwargs)
