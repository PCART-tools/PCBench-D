    def _maybe_convert_timedelta(self, other):
        if isinstance(
                other, (timedelta, np.timedelta64, Tick, np.ndarray)):
            offset = frequencies.to_offset(self.freq.rule_code)
            if isinstance(offset, Tick):
                if isinstance(other, np.ndarray):
                    nanos = np.vectorize(delta_to_nanoseconds)(other)
                else:
                    nanos = delta_to_nanoseconds(other)
                offset_nanos = delta_to_nanoseconds(offset)
                check = np.all(nanos % offset_nanos == 0)
                if check:
                    return nanos // offset_nanos
        elif isinstance(other, DateOffset):
            freqstr = other.rule_code
            base = frequencies.get_base_alias(freqstr)
            if base == self.freq.rule_code:
                return other.n
            msg = _DIFFERENT_FREQ_INDEX.format(self.freqstr, other.freqstr)
            raise IncompatibleFrequency(msg)
        elif is_integer(other):
            # integer is passed to .shift via
            # _add_datetimelike_methods basically
            # but ufunc may pass integer to _add_delta
            return other
        # raise when input doesn't have freq
        msg = "Input has different freq from PeriodIndex(freq={0})"
        raise IncompatibleFrequency(msg.format(self.freqstr))
