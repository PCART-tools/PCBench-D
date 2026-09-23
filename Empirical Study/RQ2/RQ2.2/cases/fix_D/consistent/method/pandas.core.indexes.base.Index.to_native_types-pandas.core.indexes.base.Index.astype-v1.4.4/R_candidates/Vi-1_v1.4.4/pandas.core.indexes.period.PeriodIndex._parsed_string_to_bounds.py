    def _parsed_string_to_bounds(self, reso: Resolution, parsed: datetime):
        grp = reso.freq_group
        iv = Period(parsed, freq=grp.value)
        return (iv.asfreq(self.freq, how="start"), iv.asfreq(self.freq, how="end"))
