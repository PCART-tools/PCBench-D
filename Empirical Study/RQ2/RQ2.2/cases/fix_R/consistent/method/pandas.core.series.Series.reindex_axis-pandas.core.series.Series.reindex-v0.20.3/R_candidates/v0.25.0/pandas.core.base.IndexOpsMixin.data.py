    @property
    def data(self):
        """
        Return the data pointer of the underlying data.

        .. deprecated:: 0.23.0
        """
        warnings.warn(
            "{obj}.data is deprecated and will be removed "
            "in a future version".format(obj=type(self).__name__),
            FutureWarning,
            stacklevel=2,
        )
        return self.values.data
