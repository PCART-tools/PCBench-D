    def _add_delta_td(self, other):
        assert isinstance(other, (timedelta, np.timedelta64, Tick))
        nanos = delta_to_nanoseconds(other)
        own_offset = frequencies.to_offset(self.freq.rule_code)

        if isinstance(own_offset, Tick):
            offset_nanos = delta_to_nanoseconds(own_offset)
            if np.all(nanos % offset_nanos == 0):
                return self.shift(nanos // offset_nanos)

        # raise when input doesn't have freq
        raise IncompatibleFrequency("Input has different freq from "
                                    "{cls}(freq={freqstr})"
                                    .format(cls=type(self).__name__,
                                            freqstr=self.freqstr))
