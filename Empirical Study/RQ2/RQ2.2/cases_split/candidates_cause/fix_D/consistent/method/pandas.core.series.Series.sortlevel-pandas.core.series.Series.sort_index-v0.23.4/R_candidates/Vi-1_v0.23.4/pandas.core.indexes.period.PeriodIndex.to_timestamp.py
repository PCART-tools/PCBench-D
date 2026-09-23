    def to_timestamp(self, freq=None, how='start'):
        """
        Cast to DatetimeIndex

        Parameters
        ----------
        freq : string or DateOffset, optional
            Target frequency. The default is 'D' for week or longer,
            'S' otherwise
        how : {'s', 'e', 'start', 'end'}

        Returns
        -------
        DatetimeIndex
        """
        how = _validate_end_alias(how)

        if freq is None:
            base, mult = _gfc(self.freq)
            freq = frequencies.get_to_timestamp_base(base)
        else:
            freq = Period._maybe_convert_freq(freq)

        base, mult = _gfc(freq)
        new_data = self.asfreq(freq, how)

        new_data = period.periodarr_to_dt64arr(new_data._ndarray_values, base)
        return DatetimeIndex(new_data, freq='infer', name=self.name)
