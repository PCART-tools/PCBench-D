    def _add_offset(self, other):
        assert not isinstance(other, Tick)
        base = frequencies.get_base_alias(other.rule_code)
        if base != self.freq.rule_code:
            msg = _DIFFERENT_FREQ_INDEX.format(self.freqstr, other.freqstr)
            raise IncompatibleFrequency(msg)
        return self.shift(other.n)
