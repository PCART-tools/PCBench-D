    def _sub_period(self, other):
        if self.freq != other.freq:
            msg = _DIFFERENT_FREQ_INDEX.format(self.freqstr, other.freqstr)
            raise IncompatibleFrequency(msg)

        asi8 = self.asi8
        new_data = asi8 - other.ordinal

        if self.hasnans:
            new_data = new_data.astype(np.float64)
            new_data[self._isnan] = np.nan
        # result must be Int64Index or Float64Index
        return Index(new_data)
