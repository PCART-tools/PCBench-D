    def item(self):
        """
        Return the first element of the underlying data as a Python scalar.

        Returns
        -------
        scalar
            The first element of %(klass)s.

        Raises
        ------
        ValueError
            If the data is not length-1.
        """
        if len(self) == 1:
            return next(iter(self))
        raise ValueError("can only convert an array of size 1 to a Python scalar")
