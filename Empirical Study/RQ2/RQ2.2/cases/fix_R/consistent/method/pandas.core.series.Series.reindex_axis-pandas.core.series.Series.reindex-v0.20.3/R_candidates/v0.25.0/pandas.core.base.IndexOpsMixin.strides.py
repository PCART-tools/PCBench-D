    @property
    def strides(self):
        """
        Return the strides of the underlying data.

        .. deprecated:: 0.23.0
        """
        warnings.warn(
            "{obj}.strides is deprecated and will be removed "
            "in a future version".format(obj=type(self).__name__),
            FutureWarning,
            stacklevel=2,
        )
        return self._ndarray_values.strides
