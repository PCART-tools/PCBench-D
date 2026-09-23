    def _get_string_slice(self, key):
        if not self.is_monotonic:
            raise ValueError("Partial indexing only valid for ordered time series")

        key, parsed, reso = parse_time_string(key, self.freq)
        grp = resolution.Resolution.get_freq_group(reso)
        freqn = resolution.get_freq_group(self.freq)
        if reso in ["day", "hour", "minute", "second"] and not grp < freqn:
            raise KeyError(key)

        t1, t2 = self._parsed_string_to_bounds(reso, parsed)
        return slice(
            self.searchsorted(t1, side="left"), self.searchsorted(t2, side="right")
        )
