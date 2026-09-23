    def _parsed_string_to_bounds(self, reso: Resolution, parsed: datetime):
        iv = Period(parsed, freq=reso.attr_abbrev)
        return (iv.asfreq(self.freq, how="start"), iv.asfreq(self.freq, how="end"))
