    def _check_compatible_with(
        self, other: DTScalarOrNaT, setitem: bool = False
    ) -> None:
        """
        Verify that `self` and `other` are compatible.

        * DatetimeArray verifies that the timezones (if any) match
        * PeriodArray verifies that the freq matches
        * Timedelta has no verification

        In each case, NaT is considered compatible.

        Parameters
        ----------
        other
        setitem : bool, default False
            For __setitem__ we may have stricter compatibility restrictions than
            for comparisons.

        Raises
        ------
        Exception
        """
        raise AbstractMethodError(self)
