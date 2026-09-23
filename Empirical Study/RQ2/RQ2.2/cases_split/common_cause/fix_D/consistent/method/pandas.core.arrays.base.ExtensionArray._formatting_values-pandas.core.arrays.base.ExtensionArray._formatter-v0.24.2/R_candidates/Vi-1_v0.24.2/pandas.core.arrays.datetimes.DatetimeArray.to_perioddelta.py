    def to_perioddelta(self, freq):
        """
        Calculate TimedeltaArray of difference between index
        values and index converted to PeriodArray at specified
        freq. Used for vectorized offsets

        Parameters
        ----------
        freq : Period frequency

        Returns
        -------
        TimedeltaArray/Index
        """
        # TODO: consider privatizing (discussion in GH#23113)
        from pandas.core.arrays.timedeltas import TimedeltaArray
        i8delta = self.asi8 - self.to_period(freq).to_timestamp().asi8
        m8delta = i8delta.view('m8[ns]')
        return TimedeltaArray(m8delta)
