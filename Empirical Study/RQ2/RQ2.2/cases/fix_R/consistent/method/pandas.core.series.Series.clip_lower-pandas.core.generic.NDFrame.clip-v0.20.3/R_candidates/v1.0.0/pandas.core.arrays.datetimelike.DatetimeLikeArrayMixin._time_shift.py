    def _time_shift(self, periods, freq=None):
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
        if freq is not None and freq != self.freq:
            if isinstance(freq, str):
                freq = frequencies.to_offset(freq)
            offset = periods * freq
            result = self + offset
            return result

        if periods == 0:
            # immutable so OK
            return self.copy()

        if self.freq is None:
            raise NullFrequencyError("Cannot shift with no freq")

        start = self[0] + periods * self.freq
        end = self[-1] + periods * self.freq

        # Note: in the DatetimeTZ case, _generate_range will infer the
        #  appropriate timezone from `start` and `end`, so tz does not need
        #  to be passed explicitly.
        return self._generate_range(start=start, end=end, periods=None, freq=self.freq)
