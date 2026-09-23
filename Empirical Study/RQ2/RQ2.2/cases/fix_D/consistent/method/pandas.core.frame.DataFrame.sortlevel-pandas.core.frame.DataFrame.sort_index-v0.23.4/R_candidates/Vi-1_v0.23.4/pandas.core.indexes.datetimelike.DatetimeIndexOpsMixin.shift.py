    def shift(self, n, freq=None):
        """
        Specialized shift which produces a DatetimeIndex

        Parameters
        ----------
        n : int
            Periods to shift by
        freq : DateOffset or timedelta-like, optional

        Returns
        -------
        shifted : DatetimeIndex
        """
        if freq is not None and freq != self.freq:
            if isinstance(freq, compat.string_types):
                freq = frequencies.to_offset(freq)
            offset = n * freq
            result = self + offset

            if hasattr(self, 'tz'):
                result._tz = self.tz

            return result

        if n == 0:
            # immutable so OK
            return self

        if self.freq is None:
            raise NullFrequencyError("Cannot shift with no freq")

        start = self[0] + n * self.freq
        end = self[-1] + n * self.freq
        attribs = self._get_attributes_dict()
        attribs['start'] = start
        attribs['end'] = end
        return type(self)(**attribs)
