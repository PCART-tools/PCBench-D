    def to_timestamp(self, freq=None, how: str = "start") -> DatetimeArray:
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

        how = libperiod.validate_end_alias(how)

        end = how == "E"
        if end:
            if freq == "B" or self.freq == "B":
                # roll forward to ensure we land on B date
                adjust = Timedelta(1, "D") - Timedelta(1, "ns")
                return self.to_timestamp(how="start") + adjust
            else:
                adjust = Timedelta(1, "ns")
                return (self + self.freq).to_timestamp(how="start") - adjust

        if freq is None:
            freq = self._get_to_timestamp_base()
            base = freq
        else:
            freq = Period._maybe_convert_freq(freq)
            base = freq._period_dtype_code

        new_parr = self.asfreq(freq, how=how)

        new_data = libperiod.periodarr_to_dt64arr(new_parr.asi8, base)
        dta = DatetimeArray(new_data)

        if self.freq.name == "B":
            # See if we can retain BDay instead of Day in cases where
            #  len(self) is too small for infer_freq to distinguish between them
            diffs = libalgos.unique_deltas(self.asi8)
            if len(diffs) == 1:
                diff = diffs[0]
                if diff == self.freq.n:
                    dta._freq = self.freq
                elif diff == 1:
                    dta._freq = self.freq.base
                # TODO: other cases?
            return dta
        else:
            return dta._with_freq("infer")
