    def _parse_with_reso(self, label: str):
        # overridden by TimedeltaIndex
        try:
            if self.freq is None or hasattr(self.freq, "rule_code"):
                freq = self.freq
        except NotImplementedError:
            freq = getattr(self, "freqstr", getattr(self, "inferred_freq", None))
        parsed, reso_str = parsing.parse_time_string(label, freq)
        reso = Resolution.from_attrname(reso_str)
        return parsed, reso
