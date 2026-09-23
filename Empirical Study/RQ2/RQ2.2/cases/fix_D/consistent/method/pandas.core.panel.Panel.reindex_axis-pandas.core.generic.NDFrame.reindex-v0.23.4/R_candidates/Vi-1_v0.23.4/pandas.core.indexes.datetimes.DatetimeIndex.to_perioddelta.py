    def to_perioddelta(self, freq):
        """
        Calculate TimedeltaIndex of difference between index
        values and index converted to periodIndex at specified
        freq. Used for vectorized offsets

        Parameters
        ----------
        freq: Period frequency

        Returns
        -------
        y: TimedeltaIndex
        """
        return to_timedelta(self.asi8 - self.to_period(freq)
                            .to_timestamp().asi8)
