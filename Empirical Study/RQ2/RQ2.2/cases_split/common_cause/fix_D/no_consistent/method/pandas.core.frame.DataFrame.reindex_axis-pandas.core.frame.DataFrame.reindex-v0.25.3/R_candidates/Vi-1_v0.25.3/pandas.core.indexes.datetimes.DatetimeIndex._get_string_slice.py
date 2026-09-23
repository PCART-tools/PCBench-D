    def _get_string_slice(self, key, use_lhs=True, use_rhs=True):
        freq = getattr(self, "freqstr", getattr(self, "inferred_freq", None))
        _, parsed, reso = parsing.parse_time_string(key, freq)
        loc = self._partial_date_slice(reso, parsed, use_lhs=use_lhs, use_rhs=use_rhs)
        return loc
