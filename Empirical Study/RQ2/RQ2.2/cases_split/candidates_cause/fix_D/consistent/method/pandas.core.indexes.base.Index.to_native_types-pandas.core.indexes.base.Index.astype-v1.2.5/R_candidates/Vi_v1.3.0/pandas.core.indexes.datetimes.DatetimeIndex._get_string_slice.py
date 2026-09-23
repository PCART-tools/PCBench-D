    def _get_string_slice(self, key: str):
        freq = getattr(self, "freqstr", getattr(self, "inferred_freq", None))
        parsed, reso_str = parsing.parse_time_string(key, freq)
        reso = Resolution.from_attrname(reso_str)
        return self._partial_date_slice(reso, parsed)
