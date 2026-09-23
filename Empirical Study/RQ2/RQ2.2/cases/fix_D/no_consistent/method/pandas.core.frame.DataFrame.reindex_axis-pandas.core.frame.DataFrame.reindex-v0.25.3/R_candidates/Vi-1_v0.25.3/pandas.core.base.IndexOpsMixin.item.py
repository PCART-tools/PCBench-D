    def item(self):
        """
        Return the first element of the underlying data as a python scalar.

        .. deprecated 0.25.0

        Returns
        -------
        scalar
            The first element of %(klass)s.
        """
        warnings.warn(
            "`item` has been deprecated and will be removed in a " "future version",
            FutureWarning,
            stacklevel=2,
        )
        return self.values.item()
