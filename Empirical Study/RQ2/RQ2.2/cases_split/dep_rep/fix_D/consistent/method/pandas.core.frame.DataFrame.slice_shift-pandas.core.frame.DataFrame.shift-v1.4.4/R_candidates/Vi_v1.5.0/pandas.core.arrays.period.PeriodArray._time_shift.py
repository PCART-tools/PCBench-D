    def _time_shift(self, periods: int, freq=None) -> PeriodArray:
        """
        Shift each value by `periods`.

        Note this is different from ExtensionArray.shift, which
        shifts the *position* of each element, padding the end with
        missing values.

        Parameters
        ----------
        periods : int
            Number of periods to shift by.
        freq : pandas.DateOffset, pandas.Timedelta, or str
            Frequency increment to shift by.
        """
        if freq is not None:
            raise TypeError(
                "`freq` argument is not supported for "
                f"{type(self).__name__}._time_shift"
            )
        return self + periods
