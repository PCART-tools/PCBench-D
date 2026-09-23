    @property
    def na_value(self) -> "Scalar":
        """
        BooleanDtype uses :attr:`pandas.NA` as the missing NA value.

        .. warning::

           `na_value` may change in a future release.
        """
        return libmissing.NA
