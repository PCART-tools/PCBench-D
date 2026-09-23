    def _maybe_convert_timedelta(self, other):
        if isinstance(other, (timedelta, np.timedelta64, offsets.Tick)):
            offset = frequencies.to_offset(self.freq.rule_code)
            if isinstance(offset, offsets.Tick):
                nanos = tslib._delta_to_nanoseconds(other)
                offset_nanos = tslib._delta_to_nanoseconds(offset)
                if nanos % offset_nanos == 0:
                    return nanos // offset_nanos
        elif isinstance(other, offsets.DateOffset):
            freqstr = other.rule_code
            base = frequencies.get_base_alias(freqstr)
            if base == self.freq.rule_code:
                return other.n
            msg = _DIFFERENT_FREQ_INDEX.format(self.freqstr, other.freqstr)
            raise IncompatibleFrequency(msg)
        elif isinstance(other, np.ndarray):
            if is_integer_dtype(other):
                return other
            elif is_timedelta64_dtype(other):
                offset = frequencies.to_offset(self.freq)
                if isinstance(offset, offsets.Tick):
                    nanos = tslib._delta_to_nanoseconds(other)
                    offset_nanos = tslib._delta_to_nanoseconds(offset)
                    if (nanos % offset_nanos).all() == 0:
                        return nanos // offset_nanos
        elif is_integer(other):
            # integer is passed to .shift via
            # _add_datetimelike_methods basically
            # but ufunc may pass integer to _add_delta
            return other
        # raise when input doesn't have freq
        msg = "Input has different freq from PeriodIndex(freq={0})"
        raise IncompatibleFrequency(msg.format(self.freqstr))
