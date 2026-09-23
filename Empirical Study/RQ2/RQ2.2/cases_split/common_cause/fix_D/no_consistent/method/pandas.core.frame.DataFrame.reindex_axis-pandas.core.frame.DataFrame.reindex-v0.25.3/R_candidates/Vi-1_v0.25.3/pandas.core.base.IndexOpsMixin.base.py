    @property
    def base(self):
        """
        Return the base object if the memory of the underlying data is shared.

        .. deprecated:: 0.23.0
        """
        warnings.warn(
            "{obj}.base is deprecated and will be removed "
            "in a future version".format(obj=type(self).__name__),
            FutureWarning,
            stacklevel=2,
        )
        return self.values.base
