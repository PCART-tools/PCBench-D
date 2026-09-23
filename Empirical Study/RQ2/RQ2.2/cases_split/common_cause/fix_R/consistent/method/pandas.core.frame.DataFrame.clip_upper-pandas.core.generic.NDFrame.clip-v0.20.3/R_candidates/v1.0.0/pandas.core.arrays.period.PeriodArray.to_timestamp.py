    def to_timestamp(self, freq=None, how="start"):
        """
        Cast to DatetimeArray/Index.

        Parameters
        ----------
        freq : str or DateOffset, optional
            Target frequency. The default is 'D' for week or longer,
            'S' otherwise.
        how : {'s', 'e', 'start', 'end'}
            Whether to use the start or end of the time period being converted.

        Returns
        -------
        DatetimeArray/Index
        """
        from pandas.core.arrays import DatetimeArray

        how = libperiod._validate_end_alias(how)

        end = how == "E"
        if end:
            if freq == "B":
                # roll forward to ensure we land on B date
                adjust = Timedelta(1, "D") - Timedelta(1, "ns")
                return self.to_timestamp(how="start") + adjust
            else:
                adjust = Timedelta(1, "ns")
                return (self + self.freq).to_timestamp(how="start") - adjust

        if freq is None:
            base, mult = libfrequencies.get_freq_code(self.freq)
            freq = libfrequencies.get_to_timestamp_base(base)
        else:
            freq = Period._maybe_convert_freq(freq)

        base, mult = libfrequencies.get_freq_code(freq)
        new_data = self.asfreq(freq, how=how)

        new_data = libperiod.periodarr_to_dt64arr(new_data.asi8, base)
        return DatetimeArray._from_sequence(new_data, freq="infer")
