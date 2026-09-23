    def to_perioddelta(self, freq):
        """
        Calcuates TimedeltaIndex of difference between index
        values and index converted to PeriodIndex at specified
        freq.  Used for vectorized offsets

        .. versionadded:: 0.17.0

        Parameters
        ----------
        freq : Period frequency

        Returns
        -------
        y : TimedeltaIndex
        """
        return to_timedelta(self.asi8 - self.to_period(freq)
                            .to_timestamp().asi8)
