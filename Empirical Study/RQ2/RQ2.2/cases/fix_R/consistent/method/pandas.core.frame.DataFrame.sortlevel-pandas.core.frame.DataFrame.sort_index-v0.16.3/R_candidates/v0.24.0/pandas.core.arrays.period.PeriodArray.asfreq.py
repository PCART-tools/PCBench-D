    def asfreq(self, freq=None, how='E'):
        """
        Convert the Period Array/Index to the specified frequency `freq`.

        Parameters
        ----------
        freq : str
            a frequency
        how : str {'E', 'S'}
            'E', 'END', or 'FINISH' for end,
            'S', 'START', or 'BEGIN' for start.
            Whether the elements should be aligned to the end
            or start within pa period. January 31st ('END') vs.
            January 1st ('START') for example.

        Returns
        -------
        new : Period Array/Index with the new frequency

        Examples
        --------
        >>> pidx = pd.period_range('2010-01-01', '2015-01-01', freq='A')
        >>> pidx
        <class 'pandas.core.indexes.period.PeriodIndex'>
        [2010, ..., 2015]
        Length: 6, Freq: A-DEC

        >>> pidx.asfreq('M')
        <class 'pandas.core.indexes.period.PeriodIndex'>
        [2010-12, ..., 2015-12]
        Length: 6, Freq: M

        >>> pidx.asfreq('M', how='S')
        <class 'pandas.core.indexes.period.PeriodIndex'>
        [2010-01, ..., 2015-01]
        Length: 6, Freq: M
        """
        how = libperiod._validate_end_alias(how)

        freq = Period._maybe_convert_freq(freq)

        base1, mult1 = libfrequencies.get_freq_code(self.freq)
        base2, mult2 = libfrequencies.get_freq_code(freq)

        asi8 = self.asi8
        # mult1 can't be negative or 0
        end = how == 'E'
        if end:
            ordinal = asi8 + mult1 - 1
        else:
            ordinal = asi8

        new_data = period_asfreq_arr(ordinal, base1, base2, end)

        if self._hasnans:
            new_data[self._isnan] = iNaT

        return type(self)(new_data, freq=freq)
